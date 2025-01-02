"""Tests for the Index class."""

import models
from indexes import MemoryIndex


def test_index_add_marks_block_as_indexed() -> None:
    """Should mark block as indexed when added.

    Requirements:
        - Set block.indexed to True when added
        - Store block in internal mapping
        - Don't modify other block attributes
    """
    block = models.Block(
        id=models.BlockIdentifier("test"),
        parent_id=models.BlockIdentifier("parent"),
        generator=models.Generator.TEST,
    )
    assert not block.indexed

    index = MemoryIndex()
    index.add(block)

    assert block.indexed
    assert index.get(models.BlockIdentifier("test")) is block


def test_index_get_returns_none_for_missing() -> None:
    """Should return None when block ID not found.

    Requirements:
        - Return None for unknown block IDs
        - Don't modify index state
        - Don't raise exceptions
    """
    index = MemoryIndex()
    result = index.get(models.BlockIdentifier("missing"))
    assert result is None


def test_index_get_returns_exact_block() -> None:
    """Should return exact block instance that was added.

    Requirements:
        - Return same block instance that was added
        - Don't create new block instances
        - Maintain block identity
    """
    block = models.Block(
        id=models.BlockIdentifier("test"),
        parent_id=models.BlockIdentifier("parent"),
        generator=models.Generator.TEST,
    )

    index = MemoryIndex()
    index.add(block)
    result = index.get(models.BlockIdentifier("test"))

    assert result is block  # Check identity
