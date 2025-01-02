"""Tool for finding blocks in the conversation tree using XPath-like queries."""

import models
import indexes


def find(
    index: indexes.Index,
    caller: models.Block,
    query: str,
) -> models.ToolCallResult:
    """Find blocks by searching from `caller` using xpath-like query syntax.

    Args:
        index: Block index for ID lookups
        caller: Block to start search from (context block)
        query: XPath-like query string

    Examples:
        //parent::*                   # Direct parent
        ancestor::Branch[1]           # Nearest ancestor branch
        descendant::ToolCall[last()]  # Last tool call in subtree
        //Block[@labels='important' and @labels='email']  # Blocks with labels
        child::*[position() <= 5]     # First 5 children

    Returns:
        A ToolCallResult with text including the identifiers of all matching
        Blocks.
    """
    ...
