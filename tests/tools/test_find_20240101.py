import pytest
import models
import indexes
from tools.find import find, FindMode

@pytest.fixture
def test_tree(index):
    """Creates a test tree structure with various block types and relationships."""
    root = models.Root(
        id=models.BlockIdentifier("root"),
        generator=models.Generator.TEST
    )
    
    # Add branches
    branch1 = models.Branch(
        id=models.BlockIdentifier("branch1"),
        parent_id=root.id,
        generator=models.Generator.TEST,
        tool_source_id=None
    )
    branch2 = models.Branch(
        id=models.BlockIdentifier("branch2"),
        parent_id=root.id,
        generator=models.Generator.TEST,
        tool_source_id=None
    )
    
    # Add tool calls and responses
    tool_call = models.ToolCall(
        id=models.ToolCallIdentifier("tool1"),
        parent_id=models.ModelResponseIdentifier("resp1"),
        generator=models.Generator.TEST,
        function_name="test",
        function_args={},
        provider_id=models.ToolProviderIdentifier("provider1")
    )
    
    response = models.ModelResponse(
        id=models.ModelResponseIdentifier("resp1"),
        parent_id=models.UserInputIdentifier("user1"),
        generator=models.Generator.TEST,
        text="test response",
        model="test",
        temperature=0.7,
        max_tokens=100
    )
    
    # Set up relationships
    root.children = [branch1.id, branch2.id]
    branch1.children = [tool_call.id]
    tool_call.children = [response.id]
    
    # Add labels for testing
    branch1.labels.add("important")
    response.labels.add("flagged")
    
    # Add all blocks to index
    for block in [root, branch1, branch2, tool_call, response]:
        index.add(block)
    
    return root

def test_all_axes(test_tree, index):
    """Test all supported XPath axes."""
    # Get a reference block for testing
    tool_call = index.get(models.ToolCallIdentifier("tool1"))
    
    assert find(index, tool_call, "self::*") == tool_call
    assert find(index, tool_call, "parent::*").id == "branch1"
    assert find(index, tool_call, "ancestor::Root") == test_tree
    assert find(index, tool_call, "ancestor-or-self::*") == tool_call
    assert find(index, test_tree, "descendant::ToolCall") == tool_call
    assert find(index, test_tree, "child::Branch", mode=FindMode.COLLECT)

def test_node_type_filtering(test_tree, index):
    """Test filtering by node type."""
    assert isinstance(find(index, test_tree, "descendant::Branch"), models.Branch)
    assert isinstance(
        find(index, test_tree, "descendant::ToolCall"), 
        models.ToolCall
    )
    assert isinstance(
        find(index, test_tree, "descendant::ModelResponse"), 
        models.ModelResponse
    )
    
    # Test with invalid node type
    with pytest.raises(ValueError):
        find(index, test_tree, "descendant::InvalidType")

def test_predicate_filtering(test_tree, index):
    """Test all supported predicate types."""
    # Test ID predicates
    assert find(index, test_tree, "descendant::*[@id='branch1']").id == "branch1"
    
    # Test label predicates
    assert find(
        index, 
        test_tree, 
        "descendant::*[@labels='important']"
    ).id == "branch1"
    assert find(
        index, 
        test_tree, 
        "descendant::*[@labels='flagged']"
    ).id == "resp1"
    
    # Test position predicates
    branches = find(
        index, test_tree, "child::Branch", mode=FindMode.COLLECT
    )
    assert len(branches) == 2
    assert find(index, test_tree, "child::Branch[1]").id == "branch1"
    assert find(index, test_tree, "child::Branch[2]").id == "branch2"

def test_collect_mode(test_tree, index):
    """Test collecting multiple results."""
    # Test collecting all branches
    branches = find(
        index, test_tree, "descendant::Branch", mode=FindMode.COLLECT
    )
    assert len(branches) == 2
    assert all(isinstance(b, models.Branch) for b in branches)
    
    # Test collecting with predicates
    labeled = find(
        index, 
        test_tree, 
        "descendant::*[@labels='important']", 
        mode=FindMode.COLLECT
    )
    assert len(labeled) == 1
    assert labeled[0].id == "branch1"

def test_error_cases(test_tree, index):
    """Test error handling."""
    # Invalid query syntax
    with pytest.raises(ValueError):
        find(index, test_tree, "invalid query")
    
    # No matches
    assert find(index, test_tree, "child::ModelResponse") is None
    assert find(
        index, test_tree, "child::ModelResponse", mode=FindMode.COLLECT
    ) == []
    
    # Invalid predicates
    with pytest.raises(ValueError):
        find(index, test_tree, "child::*[@invalid='value']")

def test_complex_queries(test_tree, index):
    """Test more complex query combinations."""
    # Find labeled branches
    assert find(
        index, 
        test_tree, 
        "descendant::Branch[@labels='important']"
    ).id == "branch1"
    
    # Find first child branch
    assert find(index, test_tree, "child::Branch[1]").id == "branch1"
    
    # Find responses under tool calls
    response = find(
        index, 
        test_tree, 
        "descendant::ModelResponse"
    )
    assert response.id == "resp1"
