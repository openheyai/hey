"""Tests for the find tool."""

import datetime
import pytest
import models
import indexes

from tools import find


def test_find_returns_none_for_missing_block(index: indexes.Index) -> None:
    """Should return None when target block ID is not found.

    Requirements:
        - Return None if target ID doesn't exist
        - Don't modify any blocks
        - Don't raise exceptions
    """
    root = models.Root(
        id=models.BlockIdentifier("root"), generator=models.Generator.TEST
    )
    index.add(root)

    result = find.find(index, root, target_id=models.BlockIdentifier("missing"))
    assert result is None


def test_find_returns_caller_if_target(index: indexes.Index) -> None:
    """Should return caller block if it matches target ID.

    Requirements:
        - Return caller if its ID matches target
        - Don't search other blocks unnecessarily
    """
    block = models.Block(
        id=models.BlockIdentifier("test"),
        parent_id=models.BlockIdentifier("parent"),
        generator=models.Generator.TEST,
    )
    index.add(block)

    result = find.find(index, block, target_id=models.BlockIdentifier("test"))
    assert result is block


def test_find_returns_none_if_disconnected(index: indexes.Index) -> None:
    """Should return None if blocks are not connected to root.

    Requirements:
        - Return None if blocks form disconnected graph
        - Don't modify any blocks
        - Don't raise exceptions
    """
    root = models.Root(
        id=models.BlockIdentifier("root"), generator=models.Generator.TEST
    )
    caller = models.Block(
        id=models.BlockIdentifier("caller"),
        parent_id=root.id,
        generator=models.Generator.TEST,
    )
    detached = models.Block(
        id=models.BlockIdentifier("detached"),
        parent_id=root.id,
        generator=models.Generator.TEST,
    )
    target = models.Block(
        id=models.BlockIdentifier("target"),
        parent_id=caller.id,
        generator=models.Generator.TEST,
    )

    root.children = [caller.id, detached.id]
    caller.children = [target.id]

    index.add(root)
    index.add(caller)
    index.add(target)
    index.add(detached)

    #    assert find.find(index, caller, target_id=target.id) is target
    assert find.find(index, caller, target_id=detached.id) is None


def test_find_traverses_to_child(index: indexes.Index) -> None:
    """Should find target block in child position.

    Requirements:
        - Traverse child relationships to find target
        - Return exact target block instance
        - Don't modify any blocks
    """
    root = models.Root(
        id=models.BlockIdentifier("root"), generator=models.Generator.TEST
    )
    child = models.Block(
        id=models.BlockIdentifier("child"),
        parent_id=models.BlockIdentifier("root"),
        generator=models.Generator.TEST,
    )
    root.children = [models.BlockIdentifier("child")]
    index.add(root)
    index.add(child)

    result = find.find(index, root, target_id=models.BlockIdentifier("child"))
    assert result is child


@pytest.fixture
def tool_tree(index: indexes.Index) -> models.Block:
    """Creates a tree with tool providers and tool calls for testing.

    Structure:
        root
        └── tool_provider_goto
            └── tool_provider_find
                └── tool_provider_label
                    ├── branch1
                    │   └── user_input
                    │       └── model_response
                    │           └── tool_call (using goto provider)
                    │               └── tool_result
                    └── branch2
                        └── user_input
    """
    # Create root
    root = models.Root(
        id=models.BlockIdentifier("root"), generator=models.Generator.TEST
    )
    index.add(root)

    # Create tool provider chain
    goto_provider = models.ToolProvider(
        id=models.ToolProviderIdentifier(models.BlockIdentifier("tp-goto")),
        name="goto",
        parent_id=root.id,
        generator=models.Generator.TEST,
        callable=lambda x: x,
    )
    index.add(goto_provider)
    root.children = [goto_provider.id]

    find_provider = models.ToolProvider(
        id=models.ToolProviderIdentifier(models.BlockIdentifier("tp-find")),
        name="find",
        parent_id=goto_provider.id,
        generator=models.Generator.TEST,
        callable=lambda x: x,
    )
    index.add(find_provider)
    goto_provider.children = [find_provider.id]

    label_provider = models.ToolProvider(
        id=models.ToolProviderIdentifier(models.BlockIdentifier("tp-label")),
        name="label",
        parent_id=find_provider.id,
        generator=models.Generator.TEST,
        callable=lambda x: x,
    )
    index.add(label_provider)
    find_provider.children = [label_provider.id]

    # Create branches
    branch1 = models.Branch(
        id=models.BranchIdentifier(models.BlockIdentifier("branch1")),
        parent_id=label_provider.id,
        generator=models.Generator.TEST,
        tool_source_id=None,
    )
    index.add(branch1)

    branch2 = models.Branch(
        id=models.BranchIdentifier(models.BlockIdentifier("branch2")),
        parent_id=label_provider.id,
        generator=models.Generator.TEST,
        tool_source_id=None,
    )
    index.add(branch2)
    label_provider.children = [branch1.id, branch2.id]

    # Create branch1 chain
    user_input = models.UserInput(
        id=models.UserInputIdentifier(models.BlockIdentifier("user1")),
        parent_id=branch1.id,
        generator=models.Generator.TEST,
        tool_source_id=None,
        text="test input",
    )
    index.add(user_input)
    branch1.children = [user_input.id]

    model_response = models.ModelResponse(
        id=models.ModelResponseIdentifier(models.BlockIdentifier("response1")),
        parent_id=user_input.id,
        generator=models.Generator.TEST,
        text="test response",
        model="test",
        temperature=0,
        max_tokens=100,
    )
    index.add(model_response)
    user_input.children = [model_response.id]

    tool_call = models.ToolCall(
        id=models.ToolCallIdentifier(models.BlockIdentifier("tool_call1")),
        parent_id=model_response.id,
        generator=models.Generator.TEST,
        function_name="goto",
        function_args={},
        provider_id=goto_provider.id,
    )
    index.add(tool_call)
    model_response.children = [tool_call.id]

    tool_result = models.ToolCallResult(
        id=models.ToolCallResultIdentifier(
            models.BlockIdentifier("tool_result1")
        ),
        parent_id=tool_call.id,
        generator=models.Generator.TEST,
        tool_call_id=tool_call.id,
        called_at=datetime.datetime.now(),
        text="test result",
        error=False,
        result=None,
    )
    index.add(tool_result)
    tool_call.children = [tool_result.id]

    # Create branch2 chain
    user_input2 = models.UserInput(
        id=models.UserInputIdentifier(models.BlockIdentifier("user2")),
        parent_id=branch2.id,
        generator=models.Generator.TEST,
        tool_source_id=None,
        text="test input 2",
    )
    index.add(user_input2)
    branch2.children = [user_input2.id]

    return root


def test_chain_relationships(
    tool_tree: models.Block, index: indexes.Index
) -> None:
    """Should verify the exact chain relationships in the tree.

    Requirements:
        - Tool providers form a single-child chain from root
        - Branches are siblings under last tool provider
        - Each conversation branch maintains proper single-child chains
        - Tool calls can find their providers up the ancestry chain
    """
    # Verify tool provider chain
    goto_provider = find.find(
        index, tool_tree, "child::ToolProvider", collect=False
    )
    assert goto_provider is not None
    assert goto_provider.name == "goto"

    find_provider = find.find(
        index, goto_provider, "child::ToolProvider", collect=False
    )
    assert find_provider is not None
    assert find_provider.name == "find"

    label_provider = find.find(
        index, find_provider, "child::ToolProvider", collect=False
    )
    assert label_provider is not None
    assert label_provider.name == "label"

    # Verify branches are siblings
    branches = find.find(index, label_provider, "child::Branch", collect=True)
    assert len(branches) == 2

    # Verify single-child chain in branch1
    branch1 = next(
        b for b in branches if b.id == models.BranchIdentifier("branch1")
    )
    user1 = find.find(index, branch1, "child::UserInput", collect=False)
    assert user1 is not None

    response = find.find(index, user1, "child::ModelResponse", collect=False)
    assert response is not None

    tool_call = find.find(index, response, "child::ToolCall", collect=False)
    assert tool_call is not None

    tool_result = find.find(
        index, tool_call, "child::ToolCallResult", collect=False
    )
    assert tool_result is not None

    # Verify tool call can find its provider
    provider_query = f"ancestor::ToolProvider[@id='{tool_call.provider_id}']"
    provider = find.find(index, tool_call, provider_query, collect=False)
    assert provider is goto_provider
