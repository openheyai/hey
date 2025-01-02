"""Tool for dumping a block tree to a file."""

import models


def dump(
    caller: models.Block, target_id: models.BlockIdentifier, filepath: str
) -> models.Block:
    """Dumps a block tree starting at the specified nick to a JSON file.

    Args:
        caller: The calling block
        target_nick: Nick of the block to dump
        filepath: Path where to save the dump file

    Returns:
        The target block that was dumped

    Raises:
        ValueError: If target block not found or file operations fail
    """
    ...
