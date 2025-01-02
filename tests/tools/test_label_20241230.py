"""Tests for the label tool functionality.

This test suite verifies the label tool's ability to add and remove labels
from blocks in the block tree.
"""

import pytest
import models
from tools.label import label


def test_label_add(index):
    """Test adding labels to a block.

    Requirements:
        - Should add new labels to target block's label set
        - Should return the modified block
    """
    # Setup test blocks
    root = models.Root(
        id=models.BlockIdentifier("root"), generator=models.Generator.TEST
    )
    caller = models.Block(
        id=models.BlockIdentifier("caller-block"),
        parent_id=root.id,
        generator=models.Generator.TEST,
    )
    target = models.Block(
        id=models.BlockIdentifier("target-block"),
        parent_id=caller.id,
        generator=models.Generator.TEST,
    )
    root.children = [caller.id]
    caller.children = [target.id]

    index.add(root)
    index.add(target)
    index.add(caller)
    # Test adding labels
    result = label(
        index,
        caller,
        name=models.BlockIdentifier("target-block"),
        labels=["test-label", "another-label"],
    )

    assert result == target
    assert "test-label" in target.labels
    assert "another-label" in target.labels
    assert not caller.labels
    assert not root.labels


def test_label_remove(index):
    """Test removing labels from a block.

    Requirements:
        - Should remove specified labels from target block's label set
        - Should not error if removing non-existent labels
        - Should return the modified block
    """
    # Setup test blocks with existing labels
    root = models.Root(
        id=models.BlockIdentifier("root"), generator=models.Generator.TEST
    )
    caller = models.Block(
        id=models.BlockIdentifier("caller-block"),
        parent_id=root.id,
        generator=models.Generator.TEST,
    )
    target = models.Block(
        id=models.BlockIdentifier("target-block"),
        parent_id=caller.id,
        generator=models.Generator.TEST,
        labels={"remove-me", "existing-label"},
    )
    root.children = [caller.id]
    caller.children = [target.id]

    index.add(root)
    index.add(target)
    index.add(caller)

    # Test removing labels
    result = label(
        index,
        caller,
        name=models.BlockIdentifier("target-block"),
        labels=["remove-me", "nonexistent-label"],
        remove=True,
    )

    assert result == target
    assert "existing-label" in target.labels
    assert "remove-me" not in target.labels
    assert "nonexisting-label" not in target.labels


def test_label_target_not_found(index):
    """Test error handling when target block is not found.

    Requirements:
        - Should raise ValueError if target nick doesn't exist
        - Error message should include the target nick
    """
    root = models.Root(
        id=models.BlockIdentifier("root"), generator=models.Generator.TEST
    )
    caller = models.Block(
        id=models.BlockIdentifier("caller-block"),
        parent_id=root.id,
        generator=models.Generator.TEST,
    )
    index.add(root)
    index.add(caller)

    with pytest.raises(ValueError) as exc:
        label(
            index,
            caller,
            name=models.BlockIdentifier("nonexistent-block"),
            labels=["test-label"],
        )

    assert "Could not find block" in str(exc.value)
    assert "nonexistent-block" in str(exc.value)
