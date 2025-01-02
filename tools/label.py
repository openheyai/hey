"""Tool for adding and removing labels from blocks."""

from typing import List
import models
from tools.find import find
import indexes


def label(
    index: indexes.Index,
    caller: models.Block,
    name: models.BlockIdentifier,
    labels: List[str],
    remove: bool = False,
) -> models.Block:
    """Add or remove labels from a block.

    Args:
        caller: The block making the tool call
        name: The identifier of the block to label
        labels: Labels to add or remove
        remove: If True, remove the labels instead of adding them

    Returns:
        The modified block
    """
    # Find the target block
    target = find(index, caller, target_id=name)
    if not target:
        raise ValueError(f"Could not find block with ID: {name}")

    # Add or remove labels
    if remove:
        target.labels.difference_update(labels)
    else:
        target.labels.update(labels)

    return target
