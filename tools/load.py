"""Tool for loading a block tree from a dump file."""

import models


def load(
    caller: models.Block,
    target_id: models.BlockIdentifer,
    filepath: str,
    replace: bool = False,
) -> models.Block:
    """Loads a block tree from a JSON dump file.

    Args:
        caller: The calling block
        target_id: ID of the block we're loading the tree into
        filepath: Path to the dump file
        replace: If True, replace the target block, if False, add as children

    Returns:
        The modified target block

    Raises:
        ValueError: If target block not found, file not found, or invalid dump data
    """
    ...
