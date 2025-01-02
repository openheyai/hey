import re
import models
import indexes


def query(
    index: indexes.Index,
    current: models.Block,
    query: str,
) -> list[models.Block]:
    """Find blocks by searching from `current` using xpath-like query syntax.

    Args:
        index: Block index for ID lookups
        caller: Block to start search from (context block)
        query: XPath-like query string

    Syntax:
        1. Axes (Search Directions):
            self::*                 # Current block only
            parent::*               # Direct parent only
            ancestor::*             # Any ancestor up the tree
            ancestor-or-self::*     # Include current block in ancestor search
            child::*                # Direct children only
            descendant::*           # Any descendant down the tree
            descendant-or-self::*   # Include current block in descendant search
            following-sibling::*    # Siblings after current
            preceding-sibling::*    # Siblings before current

        2. block Tests (Type Filtering):
            //Branch                # Any Branch block
            //ToolCall              # Any ToolCall block
            //ModelResponse         # Any ModelResponse block
            //UserInput             #
            //*                     # Any block type

        3. Predicates (Filtering):
            [@id='block-123']       # Match block ID
            [@labels='important']   # Match label
            [1]                     # First match only
            [last()]                # Last match only
            [position() <= 5]       # First 5 matches

        4. Operators in Predicates:
            =, !=                   # Equality tests
            >, <, >=, <=            # Numeric comparisons
            and, or                 # Boolean combinations
            =~                      # Regular expression matching

        5. Functions in Predicates:
            position()              # Current block's position
            last()                  # Last block's position
            not()                   # Boolean negation

    Search Behavior:
        - All searches start from the caller (context block)
        - Axis determines search direction and scope
        - Results ordered by document order (depth-first)

    Examples:
        //parent::*                   # Direct parent
        ancestor::Branch[1]           # Nearest ancestor branch
        descendant::ToolCall[last()]  # Last tool call in subtree
        //Block[@labels='important' and @labels='email']  # Blocks with labels
        child::*[position() <= 5]     # First 5 children

    Returns:
        A list of matching Blocks
    """
    # Split query into axis and node test parts
    if "::" not in query:
        raise ValueError("Query must contain axis specifier (::)")

    axis, remaining = query.split("::", 1)

    # Parse node test and predicates
    node_test = remaining
    predicates: list[str] = []
    if "[" in remaining:
        node_test, pred_part = remaining.split("[", 1)
        if not pred_part.endswith("]"):
            raise ValueError("Unclosed predicate bracket")
        # Split predicates and strip whitespace
        predicates = [p.strip() for p in pred_part[:-1].split(" and ")]

    # Get initial block set based on axis
    blocks = _get_axis_blocks(index, current, axis)

    # Filter by node type if specified
    if node_test != "*":
        blocks = [b for b in blocks if b.__class__.__name__ == node_test]

    # Apply predicates - each predicate further filters the previous results
    for pred in predicates:
        blocks = _apply_predicate(blocks, pred)
        
    return blocks


def _get_axis_blocks(
    index: indexes.Index,
    current: models.Block,
    axis: str,
) -> list[models.Block]:
    """Get blocks for the specified axis."""
    match axis:
        case "self":
            return [current]

        case "parent":
            if current.parent_id:
                parent = index.get(current.parent_id)
                return [parent] if parent else []
            return []

        case "ancestor":
            results = []
            block = current
            while block.parent_id:
                parent = index.get(block.parent_id)
                if parent:
                    results.append(parent)
                    block = parent
                else:
                    break
            return results

        case "ancestor-or-self":
            return [current] + _get_axis_blocks(index, current, "ancestor")

        case "child":
            return [
                child
                for id in current.children
                if (child := index.get(id)) is not None
            ]

        case "descendant":
            results = []
            to_process = current.children.copy()
            while to_process:
                child_id = to_process.pop()
                child = index.get(child_id)
                if child:
                    results.append(child)
                    to_process.extend(child.children)
            return results

        case "descendant-or-self":
            return [current] + _get_axis_blocks(index, current, "descendant")

        case _:
            raise ValueError(f"Unknown axis: {axis}")


def _apply_predicate(
    blocks: list[models.Block], pred: str
) -> list[models.Block]:
    """Apply a predicate filter to the block list."""
    # Handle position predicates
    if pred.isdigit():
        pos = int(pred) - 1
        return [blocks[pos]] if 0 <= pos < len(blocks) else []

    if pred == "last()":
        return blocks[-1:] if blocks else []

    if pred.startswith("position()"):
        # Parse position() predicate more carefully
        pred = pred.replace(" ", "")  # Remove all spaces
        if "<=" in pred:
            num = int(pred.split("<=")[1])
            return blocks[:num]
        elif ">=" in pred:
            num = int(pred.split(">=")[1])
            return blocks[num-1:]
        elif "<" in pred:
            num = int(pred.split("<")[1])
            return blocks[:num-1]
        elif ">" in pred:
            num = int(pred.split(">")[1])
            return blocks[num:]
        elif "=" in pred:
            num = int(pred.split("=")[1])
            return [blocks[num-1]] if 0 <= num-1 < len(blocks) else []
        raise ValueError(f"Invalid position predicate operator: {pred}")

    # Handle attribute predicates
    if pred.startswith("@"):
        attr, op, value = _parse_attribute_pred(pred)

        if op == "=~":
            try:
                pattern = re.compile(value.strip("'\""))
                return [
                    b for b in blocks if _match_regex_attr(b, attr, pattern)
                ]
            except re.error:
                raise ValueError(f"Invalid regex pattern: {value}")

        return [
            b for b in blocks if _match_attr(b, attr, op, value.strip("'\""))
        ]

    raise ValueError(f"Invalid predicate: {pred}")


def _parse_attribute_pred(pred: str) -> tuple[str, str, str]:
    """Parse an attribute predicate into (attr, op, value)."""
    for op in ["=~", "=", "!=", ">=", "<=", ">", "<"]:
        if op in pred:
            attr, value = pred[1:].split(op, 1)
            return attr, op, value
    raise ValueError(f"Invalid attribute predicate: {pred}")


def _match_attr(block: models.Block, attr: str, op: str, value: str) -> bool:
    """Match a block attribute against a value."""
    if attr == "id":
        block_val = block.id
    elif attr == "labels":
        return value in block.labels
    else:
        block_val = getattr(block, attr, None)

    match op:
        case "=":
            return str(block_val) == value
        case "!=":
            return str(block_val) != value
        case _:
            raise ValueError(f"Unsupported operator for {attr}: {op}")


def _match_regex_attr(
    block: models.Block,
    attr: str,
    pattern: re.Pattern,
) -> bool:
    """Match a block attribute against a regex pattern."""
    if attr == "id":
        return bool(pattern.search(str(block.id)))
    elif attr == "labels":
        return any(pattern.search(label) for label in block.labels)
    else:
        val = getattr(block, attr, None)
        return bool(val and pattern.search(str(val)))
