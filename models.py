"""
Core data models for managing conversation state and tool interactions.

This module implements a block-based architecture for representing and managing conversational state,
tool operations, and their relationships. Each interaction or state change in the system is 
represented as a distinct block, with relationships maintained through a robust identifier system
and source tracking.

The architecture follows these key principles:
- Immutability: Blocks are immutable once created, ensuring reliable state tracking
- Provenance: All changes are tracked to their source through tool operations
- Composability: Complex operations can be built from simple blocks
- Parallelism: Support for parallel conversation threads through branching

Key concepts:
- Blocks: Atomic units representing messages, operations, and state changes
- Tools: Operations that can modify conversation state
- Sources: Tracking of tool-initiated changes to maintain provenance
- Branches: Parallel conversation threads that can be created and modified
- Activities: Records of state changes and system events
"""

import typing
from typing import Callable, List, Set
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum, auto

# Type definitions for block identifiers
BlockIdentifier = typing.NewType("BlockIdentifier", str)
ModelResponseIdentifier = typing.NewType(
    "ModelResponseIdentifier", BlockIdentifier
)
ToolCallIdentifier = typing.NewType("ToolCallIdentifier", BlockIdentifier)
ToolCallResultIdentifier = typing.NewType(
    "ToolCallResultIdentifier", BlockIdentifier
)
MultiToolCallIdentifier = typing.NewType(
    "MultiToolCallIdentifier", BlockIdentifier
)
MultiToolCallResultIdentifier = typing.NewType(
    "MultiToolCallResultIdentifier", BlockIdentifier
)
UserInputIdentifier = typing.NewType("UserInputIdentifier", BlockIdentifier)
BranchIdentifier = typing.NewType("BranchIdentifier", BlockIdentifier)
ActivityIdentifier = typing.NewType("ActivityIdentifier", BlockIdentifier)
ToolProviderIdentifier = typing.NewType(
    "ToolProviderIdentifier", BlockIdentifier
)

# Composite type for tool operation sources
ToolSourceIdentifier = typing.Union[
    ToolCallResultIdentifier, MultiToolCallResultIdentifier
]


class Generator(Enum):
    """Defines the origin of a block in the conversation pipeline.

    These values specify the component responsible for creating each block, enabling
    clear tracking of how different parts of the conversation were generated.

    Values:
        TOOLS: Block was created by system tools during operation execution
        CLAUDE: Block was generated by the language model
        USER: Block represents direct user input
        SYSTEM: Block was created during system initialization
        TEST: Block was created during system testing
    """

    TOOLS = auto()
    CLAUDE = auto()
    USER = auto()
    SYSTEM = auto()
    TEST = auto()


class Block(BaseModel):
    """Base block class representing a discrete unit in the conversation.

    Blocks are the fundamental building blocks of the conversation system. Each block
    represents an atomic unit of the conversation, whether it's a message, operation,
    or state change. Blocks maintain relationships through parent/child references
    and can be labeled for organization and filtering.

    Attributes:
        id (BlockIdentifier): Unique identifier for the block
        parent_id (BlockIdentifier): Identifier of the parent block
        children (list[BlockIdentifier]): List of child block identifiers
        created_at (datetime): Timestamp of block creation
        generator (Generator): Component that created this block
        labels (Set[str]): Set of labels applied to this block

    The block structure ensures:
        - Clear parent/child relationships for tracking conversation flow
        - Temporal ordering through creation timestamps
        - Origin tracking through the generator field
        - Flexible organization through labels
    """

    id: BlockIdentifier
    parent_id: BlockIdentifier
    children: list[BlockIdentifier] = Field(
        default_factory=list[BlockIdentifier]
    )
    created_at: datetime = Field(default_factory=datetime.now)
    generator: Generator
    labels: Set[str] = Field(default_factory=set)
    indexed: bool = (
        False  # Whether this block has been added to an index for lookup
    )


class Noop(Block):
    """Represents a no-operation block in the conversation.

    Used to maintain structural integrity in cases where a placeholder block
    is needed without performing any actual operations. This helps preserve
    the consistency of the block chain while allowing for structural flexibility.
    """

    pass


class Root(Block):
    """Represents the root of a conversation tree.

    The root block serves as the anchor point for all conversation branches and
    tool providers. It is typically created during system initialization and has
    no parent.


    Attributes:
        parent_id (None): Always None as root has no parent

    Examples:
        Creating a root node for a new conversation:
            root = Root(
                id=BlockIdentifier("summit-root"),
                parent_id=None,
                generator=Generator.TOOLS
            )

        Adding tool providers as children:
            tool = ToolProvider(
                id=ToolProviderIdentifier("summit-root.0.tp-goto"),
                name="goto",
                parent_id=BlockIdentifier("summit-root"),
                generator=Generator.SYSTEM,
                callable=lambda x: x
            )
    """

    parent_id: None = None


class End(Block):
    """Marks the end of a conversation branch.

    Used to explicitly terminate a conversation branch, ensuring proper cleanup
    and state management when a branch is completed.
    """

    pass


P = typing.ParamSpec("P")
ToolCallable = Callable[typing.Concatenate["ToolCall", P], Block | list[Block]]


class ToolProvider(Block):
    """Defines a tool that can be called to modify conversation state.

    Tool providers represent available operations that can be performed within
    the conversation. Each provider encapsulates a specific function that can
    modify the conversation state in some way.

    Attributes:
        id (ToolProviderIdentifier): Unique identifier for this tool provider
        name (str): Human-readable name of the tool
        callable (ToolCallable): Function that implements the tool's operation

    Tool providers support:
        - Registration of new conversation operations
        - Encapsulation of operation implementation details
        - Tracking of tool usage through the block system
    """

    id: ToolProviderIdentifier
    name: str
    callable: ToolCallable


class UserInput(Block):
    """Represents user input in the conversation.

    Captures both direct user interactions and system-generated user inputs
    (e.g., from tool operations). Maintains provenance through tool source
    tracking when appropriate.

    Attributes:
        id (UserInputIdentifier): Unique identifier for this input
        tool_source_id (ToolSourceIdentifier | None): Source tool if generated
        text (str | None): The actual input text

    User inputs can be:
        - Created directly from user interactions
        - Generated by tool operations (e.g., when creating a new branch)
        - Referenced by model responses and tool operations
    """

    id: UserInputIdentifier
    tool_source_id: ToolSourceIdentifier | None
    text: str | None


class ToolCall(Block):
    """Represents a request to execute a tool operation.

    Tool calls encapsulate the intent to execute a specific tool operation
    with given arguments. They can be part of a single operation or grouped
    in a MultiToolCall for parallel execution.

    Attributes:
        id (ToolCallIdentifier): Unique identifier for this tool call
        parent_id (ModelResponseIdentifier | MultiToolCallIdentifier): Parent block
        function_name (str): Name of the tool function to call
        function_args (dict): Arguments to pass to the tool function
        provider_id (ToolProviderIdentifier): ID of the tool provider

    Tool calls:
        - Link to their provider for execution
        - Maintain clear parent/child relationships
        - Support both individual and grouped execution
        - Track all arguments for reproducibility
    """

    id: ToolCallIdentifier
    parent_id: ModelResponseIdentifier | MultiToolCallIdentifier
    function_name: str
    function_args: dict
    provider_id: ToolProviderIdentifier


class MultiToolCall(Block):
    """Groups multiple tool calls that should be executed together.

    Provides a mechanism for executing multiple related tool operations as a unit.
    The calls are maintained as siblings in the block structure while preserving
    their logical grouping through the MultiToolCall container.

    Attributes:
        id (MultiToolCallIdentifier): Unique identifier for this group
        parent_id (ModelResponseIdentifier): Parent response that initiated the calls
        tool_calls (list[ToolCall]): List of tool calls to execute

    This structure supports:
        - Parallel execution of multiple operations
        - Maintenance of operation relationships
        - Clear tracking of execution results
        - Proper sequencing of related operations
    """

    id: MultiToolCallIdentifier
    parent_id: ModelResponseIdentifier
    tool_calls: list[ToolCall] = Field(default_factory=list[ToolCall])


class ToolCallResult(Block):
    """Records the result of executing a tool operation.

    Captures the outcome of a tool operation execution, including timing
    information and any errors that occurred. Results can include both
    data and new blocks created by the operation.

    Attributes:
        id (ToolCallResultIdentifier): Unique identifier for this result
        tool_call_id (ToolCallIdentifier): ID of the originating tool call
        called_at (datetime): When the tool execution began
        finished_at (datetime | None): When the tool execution completed
        text (str | None): Optional text description of the result
        result (BlockIdentifier | None): Result block
        error (str | None): Error message if the operation failed

    Results track:
        - Execution timing for performance monitoring
        - Success or failure of operations
        - New blocks or data created by the operation
        - Clear links to the originating tool call
    """

    id: ToolCallResultIdentifier
    tool_call_id: ToolCallIdentifier
    called_at: datetime
    finished_at: datetime | None = Field(default=None)
    text: str | None
    error: bool
    result: BlockIdentifier | None


class TextBlock(Block):
    """Represents a block containing arbitrary text content.

    A simple block type for storing text content within the conversation
    structure. Useful for maintaining textual information that needs to
    be referenced by other blocks.

    Attributes:
        text (str): The text content stored in this block
    """

    text: str


class MultiToolCallResult(Block):
    """Groups results from executing multiple tool calls.

    Collects and maintains the results from a parallel tool execution
    initiated by a MultiToolCall. Results maintain their independence
    while preserving their logical grouping.

    Attributes:
        id (MultiToolCallResultIdentifier): Unique identifier for this result group
        multi_tool_call_id (MultiToolCallIdentifier): ID of the originating multi-tool call
        tool_call_results (list[ToolCallResult]): Results from individual tool calls

    This structure ensures:
        - Clear tracking of parallel operation results
        - Maintenance of result relationships
        - Support for result aggregation and analysis
    """

    id: MultiToolCallResultIdentifier
    multi_tool_call_id: MultiToolCallIdentifier
    tool_call_results: list[ToolCallResult]


class Branch(Block):
    """Represents a conversation branch.

    Branches enable parallel conversation threads that can evolve independently.
    They can be created during system initialization or by tool operations,
    maintaining proper source tracking in all cases.

    Attributes:
        id (BranchIdentifier): Unique identifier for this branch
        tool_source_id (ToolSourceIdentifier | None): Source tool if created by operation

    Branches support:
        - Parallel conversation development
        - Clear tracking of branch creation
        - Independent state evolution
        - Proper relationship maintenance
    """

    id: BranchIdentifier
    tool_source_id: ToolSourceIdentifier | None


class Activity(Block):
    """Records state changes and system activities.

    Activities provide an audit trail of significant changes to the conversation
    state. Each activity maintains a reference to the tool operation that
    caused the change, ensuring clear provenance tracking.

    Attributes:
        id (ActivityIdentifier): Unique identifier for this activity
        tool_source_id (ToolSourceIdentifier): Source tool that caused the change
        description (str): Human-readable description of the activity

    Activities track:
        - State changes and their sources
        - System events and operations
        - Clear description of changes
        - Temporal ordering of operations
    """

    id: ActivityIdentifier
    tool_source_id: ToolSourceIdentifier
    description: str


class ModelResponse(Block):
    """Represents a response generated by the language model.

    Model responses can be triggered by user input or system activities and may
    include calls to tools for further operations. They form the primary means
    of system interaction with the conversation state.

    Attributes:
        id (ModelResponseIdentifier): Unique identifier for this response
        parent_id (UserInputIdentifier | ToolCallResultIdentifier | ActivityIdentifier):
            ID of the block that triggered this response
        text (str): The generated response text
        model (str): Identifier of the model used
        temperature (float): Temperature setting used for generation
        max_tokens (int): Maximum tokens allowed in the response
        tool_call_ids (List[ToolCallIdentifier]): Tools called by this response

    Responses support:
        - Clear tracking of generation parameters
        - Links to triggered tool operations
        - Proper parent/child relationships
        - Comprehensive state interaction
    """

    id: ModelResponseIdentifier
    parent_id: (
        UserInputIdentifier | ToolCallResultIdentifier | ActivityIdentifier
    )
    text: str
    model: str
    temperature: float
    max_tokens: int
    tool_call_ids: List[ToolCallIdentifier] = Field(default_factory=list)