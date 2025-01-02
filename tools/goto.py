"""Tool for navigating to blocks in the conversation tree using XPath-like queries."""

import models
import indexes


def goto(
    index: indexes.Index,
    caller: models.Block,
    query: str,
) -> models.Block:
    """Go to block by searching from `caller` using xpath-like query syntax.

    Args:
        index: Block index for ID lookups
        caller: Block to start search from (context block)
        query: XPath-like query string

    Returns:
        The Block to navigate to, or an error if multiple Blocks are returned.
    """
    ...
