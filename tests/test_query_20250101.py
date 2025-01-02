import datetime
import pytest
import indexes
import models
import query


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


def test_self_axis(tool_tree: models.Block, index: indexes.Index):
    """Test self:: axis returns only the current block."""
    user1 = index.get(models.BlockIdentifier("user1"))
    assert user1 is not None
    results = query.query(index, user1, "self::*")
    assert len(results) == 1
    assert results[0].id == user1.id


def test_parent_axis(tool_tree: models.Block, index: indexes.Index):
    """Test parent:: axis returns direct parent."""
    user1 = index.get(models.BlockIdentifier("user1"))
    assert user1 is not None
    results = query.query(index, user1, "parent::*")
    assert len(results) == 1
    assert results[0].id == models.BlockIdentifier("branch1")


def test_ancestor_axis(tool_tree: models.Block, index: indexes.Index):
    """Test ancestor:: axis returns all ancestors."""
    tool_result = index.get(models.BlockIdentifier("tool_result1"))
    assert tool_result is not None
    results = query.query(index, tool_result, "ancestor::*")
    assert len(results) > 1
    # Should include all blocks up to root
    ancestor_ids = {block.id for block in results}
    expected_ids = {
        models.BlockIdentifier("tool_call1"),
        models.BlockIdentifier("response1"),
        models.BlockIdentifier("user1"),
        models.BlockIdentifier("branch1"),
        models.BlockIdentifier("tp-label"),
        models.BlockIdentifier("tp-find"),
        models.BlockIdentifier("tp-goto"),
        models.BlockIdentifier("root"),
    }
    assert ancestor_ids == expected_ids


def test_ancestor_or_self_axis(tool_tree: models.Block, index: indexes.Index):
    """Test ancestor-or-self:: axis includes current block."""
    user1 = index.get(models.BlockIdentifier("user1"))
    assert user1 is not None
    results = query.query(index, user1, "ancestor-or-self::*")
    result_ids = {block.id for block in results}
    assert user1.id in result_ids
    assert models.BlockIdentifier("branch1") in result_ids
    assert models.BlockIdentifier("root") in result_ids


def test_child_axis(tool_tree: models.Block, index: indexes.Index):
    """Test child:: axis returns direct children."""
    branch1 = index.get(models.BlockIdentifier("branch1"))
    assert branch1 is not None
    results = query.query(index, branch1, "child::*")
    assert len(results) == 1
    assert results[0].id == models.BlockIdentifier("user1")


def test_descendant_axis(tool_tree: models.Block, index: indexes.Index):
    """Test descendant:: axis returns all descendants."""
    branch1 = index.get(models.BlockIdentifier("branch1"))
    assert branch1 is not None
    results = query.query(index, branch1, "descendant::*")
    result_ids = {block.id for block in results}
    expected_ids = {
        models.BlockIdentifier("user1"),
        models.BlockIdentifier("response1"),
        models.BlockIdentifier("tool_call1"),
        models.BlockIdentifier("tool_result1"),
    }
    assert result_ids == expected_ids


def test_block_type_filter(tool_tree: models.Block, index: indexes.Index):
    """Test filtering by block type."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None
    results = query.query(index, root, "descendant::ToolProvider")
    assert len(results) == 3
    assert all(isinstance(block, models.ToolProvider) for block in results)


def test_id_predicate(tool_tree: models.Block, index: indexes.Index):
    """Test filtering by ID predicate."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None
    results = query.query(index, root, "descendant::*[@id='tool_call1']")
    assert len(results) == 1
    assert results[0].id == models.BlockIdentifier("tool_call1")


def test_position_predicate(tool_tree: models.Block, index: indexes.Index):
    """Test position() predicate filtering."""
    label_provider = index.get(models.BlockIdentifier("tp-label"))
    assert label_provider is not None
    results = query.query(index, label_provider, "child::*[position() <= 1]")
    assert len(results) == 1
    assert results[0].id == models.BlockIdentifier("branch1")


def test_last_predicate(tool_tree: models.Block, index: indexes.Index):
    """Test last() predicate filtering."""
    label_provider = index.get(models.BlockIdentifier("tp-label"))
    assert label_provider is not None
    results = query.query(index, label_provider, "child::*[last()]")
    assert len(results) == 1
    assert results[0].id == models.BlockIdentifier("branch2")


def test_multiple_predicates(tool_tree: models.Block, index: indexes.Index):
    """Test combining multiple predicates."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None
    # Add a label to test with
    tool_call = index.get(models.BlockIdentifier("tool_call1"))
    assert tool_call is not None
    tool_call.labels.add("test_label")

    results = query.query(
        index,
        root,
        "descendant::ToolCall[@labels='test_label' and @id='tool_call1']",
    )
    assert len(results) == 1
    assert results[0].id == models.BlockIdentifier("tool_call1")


def test_empty_results(tool_tree: models.Block, index: indexes.Index):
    """Test queries that should return no results."""
    user1 = index.get(models.BlockIdentifier("user1"))
    assert user1 is not None
    results = query.query(
        index, user1, "descendant::ToolProvider"
    )  # User1 has no ToolProvider descendants
    assert len(results) == 0


def test_invalid_query_syntax(tool_tree: models.Block, index: indexes.Index):
    """Test handling of invalid query syntax."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None
    with pytest.raises(ValueError):
        query.query(index, root, "invalid::syntax::")


def test_regex_match_id(tool_tree: models.Block, index: indexes.Index):
    """Test regex matching on block IDs."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None

    # Match all tool call related blocks using regex
    results = query.query(index, root, "descendant::*[@id=~'tool_.*']")
    result_ids = {block.id for block in results}
    expected_ids = {
        models.BlockIdentifier("tool_call1"),
        models.BlockIdentifier("tool_result1"),
    }
    assert result_ids == expected_ids


def test_regex_match_labels(tool_tree: models.Block, index: indexes.Index):
    """Test regex matching on block labels."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None

    # Add some test labels
    tool_call = index.get(models.BlockIdentifier("tool_call1"))
    assert tool_call is not None
    tool_call.labels.add("test_label_1")
    tool_call.labels.add("test_label_2")

    results = query.query(
        index, root, "descendant::*[@labels=~'test_label_\\d+']"
    )
    assert len(results) == 1
    assert results[0].id == models.BlockIdentifier("tool_call1")


def test_regex_match_complex(tool_tree: models.Block, index: indexes.Index):
    """Test complex regex patterns with multiple conditions."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None

    # Add test labels to multiple blocks
    tool_call = index.get(models.BlockIdentifier("tool_call1"))
    assert tool_call is not None
    tool_call.labels.add("prefix_abc_123")

    tool_result = index.get(models.BlockIdentifier("tool_result1"))
    assert tool_result is not None
    tool_result.labels.add("prefix_def_456")

    # Match blocks with specific label pattern and ID pattern
    results = query.query(
        index,
        root,
        "descendant::*[@labels=~'prefix_.*_\\d+' and @id=~'tool_.*1']",
    )
    assert len(results) == 1
    assert results[0].id == models.BlockIdentifier("tool_call1")


def test_regex_no_matches(tool_tree: models.Block, index: indexes.Index):
    """Test regex patterns that should match nothing."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None

    results = query.query(index, root, "descendant::*[@id=~'nonexistent_.*']")
    assert len(results) == 0


def test_regex_invalid_pattern(tool_tree: models.Block, index: indexes.Index):
    """Test handling of invalid regex patterns."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None

    # Invalid regex pattern should raise ValueError
    with pytest.raises(ValueError):
        query.query(index, root, "descendant::*[@id=~'[invalid(regex']")


def test_regex_case_sensitivity(tool_tree: models.Block, index: indexes.Index):
    """Test case sensitivity in regex matching."""
    root = index.get(models.BlockIdentifier("root"))
    assert root is not None

    tool_call = index.get(models.BlockIdentifier("tool_call1"))
    assert tool_call is not None
    tool_call.labels.add("MixedCase_Label")

    # Case-sensitive match
    results = query.query(
        index, root, "descendant::*[@labels=~'Mixed.*_Label']"
    )
    assert len(results) == 1

    # Should not match different case
    results = query.query(
        index, root, "descendant::*[@labels=~'mixedcase_label']"
    )
    assert len(results) == 0
