"""Shared test fixtures."""

import pytest
import indexes


@pytest.fixture
def index() -> indexes.Index:
    """Provides a clean MemoryIndex instance for tests.

    Returns:
        A new MemoryIndex instance
    """
    return indexes.MemoryIndex()


@pytest.fixture
def sample_wip() -> None:
    # id format: "{branch_name}.{count_branch_messages}.{node_type}.{count_messages_with_same_type_on_branch}"
    # since multi tool calls and multi tool call responses are internal structures, they won't increase count_branch_messages for tool calls and tool call results they track
    from models import (
        MultiToolCallResultIdentifier,
        Root,
        Activity,
        BranchIdentifier,
        ToolProvider,
        Branch,
        UserInput,
        ToolCall,
        ToolCallResult,
        ToolCallResultIdentifier,
        ToolCallIdentifier,
        Generator,
        BlockIdentifier,
        ModelResponseIdentifier,
        MultiToolCallResult,
        MultiToolCallIdentifier,
        MultiToolCall,
        ModelResponse,
        ActivityIdentifier,
        ToolProviderIdentifier,
        UserInputIdentifier,
    )

    import datetime

    Root(
        id=BlockIdentifier("summit-root"),
        parent_id=None,
        generator=Generator.TOOLS,
    )
    ToolProvider(
        id=ToolProviderIdentifier(BlockIdentifier("summit-root.0.tp-goto")),
        name="goto",
        parent_id=BlockIdentifier("summit-root"),
        generator=Generator.SYSTEM,
        callable=lambda x: x,
    )
    ToolProvider(
        id=ToolProviderIdentifier(BlockIdentifier("summit-root.1.tp-find")),
        name="find",
        parent_id=BlockIdentifier("summit-root.0.tp-goto"),
        generator=Generator.SYSTEM,
        callable=lambda x: x,
    )
    ToolProvider(
        id=ToolProviderIdentifier(BlockIdentifier("summit-root.2.tp-fork")),
        name="fork",
        parent_id=BlockIdentifier("summit-root.1.tp-find"),
        generator=Generator.SYSTEM,
        callable=lambda x: x,
    )
    ToolProvider(
        id=ToolProviderIdentifier(BlockIdentifier("summit-root.3.tp-label")),
        name="label",
        parent_id=BlockIdentifier("summit-root.2.tp-fork"),
        generator=Generator.SYSTEM,
        callable=lambda x: x,
    )
    ToolProvider(
        id=ToolProviderIdentifier(BlockIdentifier("summit-root.4.tp-send")),
        name="send",
        parent_id=BlockIdentifier("summit-root.3.tp-label"),
        generator=Generator.SYSTEM,
        callable=lambda x: x,
    )
    ToolProvider(
        id=ToolProviderIdentifier(BlockIdentifier("summit-root.5.tp-generate")),
        name="generate",
        parent_id=BlockIdentifier("summit-root.4.tp-send"),
        generator=Generator.SYSTEM,
        callable=lambda x: x,
    )
    ToolProvider(
        id=ToolProviderIdentifier(BlockIdentifier("tool-name")),
        name="name",
        parent_id=BlockIdentifier("summit-root.5.tp-generate"),
        generator=Generator.SYSTEM,
        callable=lambda x: x,
    )
    ToolProvider(
        id=ToolProviderIdentifier(BlockIdentifier("summit-root.5.tp-set")),
        name="set",
        parent_id=BlockIdentifier("tool-name"),
        generator=Generator.SYSTEM,
        callable=lambda x: x,
    )
    ToolProvider(
        id=ToolProviderIdentifier(BlockIdentifier("summit-root.6.tp-new")),
        name="new",
        parent_id=BlockIdentifier("summit-root.5.tp-set"),
        generator=Generator.SYSTEM,
        callable=lambda x: x,
    )
    Branch(
        id=BranchIdentifier(BlockIdentifier("branch-main")),
        parent_id=BlockIdentifier("summit-root.6.tp-new"),
        generator=Generator.SYSTEM,
        tool_source_id=None,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("branch-main.0.ui.0")),
        text="let's fork and write a novel",
        parent_id=BlockIdentifier("branch-main"),
        generator=Generator.USER,
        tool_source_id=None,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("branch-main.1.mr.0")),
        text="I'll create a branch named `novel-project` from `branch-main`",
        parent_id=UserInputIdentifier(BlockIdentifier("branch-main.0.ui.0")),
        generator=Generator.CLAUDE,
        temperature=0,
        model="t1",
        max_tokens=64,
    )
    ToolCall(
        id=ToolCallIdentifier(BlockIdentifier("branch-main.2.tc.0")),
        function_name="fork",
        function_args={"from": "branch-main", "name": "novel-project"},
        provider_id=ToolProviderIdentifier(
            BlockIdentifier("summit-root.2.tp-fork")
        ),
        parent_id=ModelResponseIdentifier(
            BlockIdentifier("branch-main.1.mr.0")
        ),
        generator=Generator.CLAUDE,
    )
    ToolCallResult(
        id=ToolCallResultIdentifier(BlockIdentifier("branch-main.3.tcr.0")),
        tool_call_id=ToolCallIdentifier(BlockIdentifier("branch-main.2.tc.0")),
        result="created fork `novel-project` at `branch-main`",
        parent_id=ToolCallIdentifier(BlockIdentifier("branch-main.2.tc.0")),
        generator=Generator.TOOLS,
        called_at=datetime.datetime.now(),
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("branch-main.4.ui.1")),
        text="go to the fork",
        parent_id=ToolCallResultIdentifier(
            BlockIdentifier("branch-main.3.tcr.0")
        ),
        generator=Generator.USER,
        tool_source_id=None,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("branch-main.5.mr.1")),
        text="Activating the `novel-project` fork",
        parent_id=UserInputIdentifier(BlockIdentifier("branch-main.4.ui.1")),
        generator=Generator.CLAUDE,
        temperature=0,
        model="t1",
        max_tokens=64,
    )
    ToolCall(
        id=ToolCallIdentifier(BlockIdentifier("branch-main.6.tc.1")),
        function_name="goto",
        function_args={"name": "novel-project"},
        provider_id=ToolProviderIdentifier(
            BlockIdentifier("summit-root.0.tp-goto")
        ),
        parent_id=ModelResponseIdentifier(
            BlockIdentifier("branch-main.5.mr.1")
        ),
        generator=Generator.CLAUDE,
    )
    ToolCallResult(
        id=ToolCallResultIdentifier(BlockIdentifier("branch-main.7.tcr.1")),
        tool_call_id=ToolCallIdentifier(BlockIdentifier("branch-main.6.tc.1")),
        text="activated fork `novel-project`, switched from `branch-main`",
        parent_id=ToolCallIdentifier(BlockIdentifier("branch-main.6.tc.1")),
        called_at=datetime.datetime.now(),
        result=BlockIdentifier("novel-project"),
        generator=Generator.TOOLS,
    )
    Branch(
        id=BranchIdentifier(BlockIdentifier("novel-project")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("branch-main.3.tcr.0")
        ),
        parent_id=BlockIdentifier("branch-main"),
        generator=Generator.TOOLS,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("novel-project.0.act.0")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("branch-main.7.tcr.1")
        ),
        description="activated fork `novel-project`. switched from `branch-main`",
        parent_id=BlockIdentifier("novel-project"),
        generator=Generator.TOOLS,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("novel-project.1.ui.0")),
        text="generate 3 random names",
        parent_id=BlockIdentifier("novel-project.0.act.0"),
        generator=Generator.USER,
        tool_source_id=None,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("novel-project.2.mr.0")),
        text="Generated names: Elena Blackwood, Marcus Chen, Sophia Patel",
        parent_id=UserInputIdentifier(BlockIdentifier("novel-project.1.ui.0")),
        generator=Generator.CLAUDE,
        temperature=0,
        model="t1",
        max_tokens=64,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("novel-project.3.ui.1")),
        text="request a backstory with a branch for each of those",
        parent_id=BlockIdentifier("novel-project.2.mr.0"),
        generator=Generator.USER,
        tool_source_id=None,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("novel-project.4.mr.1")),
        text="Creating a fork for each from 'novel-project'",
        parent_id=UserInputIdentifier(BlockIdentifier("novel-project.3.ui.1")),
        generator=Generator.CLAUDE,
        temperature=0,
        model="t1",
        max_tokens=64,
    )
    MultiToolCall(
        id=MultiToolCallIdentifier(BlockIdentifier("novel-project.5.mtc.0")),
        tool_calls=[
            ToolCall(
                id=ToolCallIdentifier(BlockIdentifier("novel-project.5.tc.0")),
                function_name="fork",
                function_args={
                    "name": "elena-blackwood",
                    "from": "novel-project",
                    "prompt": "develop full backstory for 'Elena Blackwood'",
                },
                parent_id=MultiToolCallIdentifier(
                    BlockIdentifier("novel-project.5.mtc.0")
                ),
                generator=Generator.CLAUDE,
                provider_id=ToolProviderIdentifier(
                    BlockIdentifier("summit-root.2.tp-fork")
                ),
            ),
            ToolCall(
                id=ToolCallIdentifier(BlockIdentifier("novel-project.5.tc.1")),
                function_name="fork",
                function_args={
                    "name": "marcus-chen",
                    "from": "novel-project",
                    "prompt": "develop full backstory for 'Marcus Chen'",
                },
                parent_id=MultiToolCallIdentifier(
                    BlockIdentifier("novel-project.5.mtc.0")
                ),
                generator=Generator.CLAUDE,
                provider_id=ToolProviderIdentifier(
                    BlockIdentifier("summit-root.2.tp-fork")
                ),
            ),
            ToolCall(
                id=ToolCallIdentifier(BlockIdentifier("novel-project.5.tc.2")),
                function_name="fork",
                function_args={
                    "name": "sophia-patel",
                    "from": "novel-project",
                    "prompt": "develop full backstory for 'Sophia Patel'",
                },
                parent_id=MultiToolCallIdentifier(
                    BlockIdentifier("novel-project.5.mtc.0")
                ),
                generator=Generator.CLAUDE,
                provider_id=ToolProviderIdentifier(
                    BlockIdentifier("summit-root.2.tp-fork")
                ),
            ),
        ],
        parent_id=ModelResponseIdentifier(
            BlockIdentifier("novel-project.4.mr.1")
        ),
        generator=Generator.CLAUDE,
    )
    MultiToolCallResult(
        id=MultiToolCallResultIdentifier(
            BlockIdentifier("novel-project.6.mtcr.0")
        ),
        multi_tool_call_id=MultiToolCallIdentifier(
            BlockIdentifier("novel-project.5.mtc.0")
        ),
        tool_call_results=[
            ToolCallResult(
                id=ToolCallResultIdentifier(
                    BlockIdentifier("novel-project.6.tcr.0")
                ),
                tool_call_id=ToolCallIdentifier(
                    BlockIdentifier("novel-project.5.tc.0")
                ),
                text="created fork `elena-blackwood` at `novel-project`",
                parent_id=BlockIdentifier("novel-project.6.mtcr.0"),
                result=BlockIdentifier("elena-blackwood"),
                called_at=datetime.datetime.now(),
                generator=Generator.TOOLS,
            ),
            ToolCallResult(
                id=ToolCallResultIdentifier(
                    BlockIdentifier("novel-project.6.tcr.1")
                ),
                tool_call_id=ToolCallIdentifier(
                    BlockIdentifier("novel-project.5.tc.1")
                ),
                text="created fork `marcus-chen` at `novel-project`",
                parent_id=BlockIdentifier("novel-project.6.mtcr.0"),
                result=BlockIdentifier("marcus-chen"),
                called_at=datetime.datetime.now(),
                generator=Generator.TOOLS,
            ),
            ToolCallResult(
                id=ToolCallResultIdentifier(
                    BlockIdentifier("novel-project.6.tcr.2")
                ),
                tool_call_id=ToolCallIdentifier(
                    BlockIdentifier("novel-project.5.tc.2")
                ),
                text="created fork `sophia-patel` at `novel-project`",
                parent_id=BlockIdentifier("novel-project.6.mtcr.0"),
                result=BlockIdentifier("sophia-patel"),
                called_at=datetime.datetime.now(),
                generator=Generator.TOOLS,
            ),
        ],
        parent_id=BlockIdentifier("novel-project.5.mtc.0"),
        generator=Generator.TOOLS,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("novel-project.7.ui.2")),
        text="let's work on Elena's backstory",
        parent_id=BlockIdentifier("novel-project.6.mtcr.0"),
        generator=Generator.USER,
        tool_source_id=None,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("novel-project.8.mr.2")),
        text="I'll go to the `elena-blackwood` fork",
        parent_id=UserInputIdentifier(BlockIdentifier("novel-project.7.ui.2")),
        generator=Generator.CLAUDE,
        temperature=0,
        model="t1",
        max_tokens=64,
    )
    ToolCall(
        id=ToolCallIdentifier(BlockIdentifier("novel-project.9.tc.3")),
        function_name="goto",
        function_args={"name": "elena-blackwood"},
        parent_id=ModelResponseIdentifier(
            BlockIdentifier("novel-project.7.ui.2")
        ),
        generator=Generator.CLAUDE,
        provider_id=ToolProviderIdentifier(
            BlockIdentifier("summit-root.0.tp-goto")
        ),
    )
    ToolCallResult(
        id=ToolCallResultIdentifier(BlockIdentifier("novel-project.10.tcr.3")),
        tool_call_id=ToolCallIdentifier(
            BlockIdentifier("novel-project.9.tc.3")
        ),
        text="activated `elena-blackwood` fork",
        result=BlockIdentifier("elena-blackwood.1.act.0"),
        parent_id=BlockIdentifier("novel-project.9.tc.3"),
        called_at=datetime.datetime.now(),
        generator=Generator.TOOLS,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("novel-project.11.act.1")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("branch-main.7.tcr.1")
        ),
        description="activated fork `novel-project`. switched from `elena-blackwood`",
        parent_id=BlockIdentifier("novel-project"),
        generator=Generator.TOOLS,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("novel-project.12.ui.3")),
        text="generate on other forks",
        parent_id=BlockIdentifier("novel-project.11.act.1"),
        generator=Generator.USER,
        tool_source_id=None,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("novel-project.13.mr.3")),
        text="I'll generate responses for each character's backstory",
        parent_id=UserInputIdentifier(BlockIdentifier("novel-project.12.ui.3")),
        generator=Generator.CLAUDE,
        temperature=0,
        model="t1",
        max_tokens=64,
    )
    MultiToolCall(
        id=MultiToolCallIdentifier(BlockIdentifier("novel-project.14.mtc.1")),
        tool_calls=[
            ToolCall(
                id=ToolCallIdentifier(BlockIdentifier("novel-project.15.tc.4")),
                function_name="generate",
                function_args={"fork": "elena-blackwood"},
                parent_id=MultiToolCallIdentifier(
                    BlockIdentifier("novel-project.14.mtc.1")
                ),
                generator=Generator.CLAUDE,
                provider_id=ToolProviderIdentifier(
                    BlockIdentifier("summit-root.5.tp-generate")
                ),
            ),
            ToolCall(
                id=ToolCallIdentifier(BlockIdentifier("novel-project.16.tc.5")),
                function_name="generate",
                function_args={"fork": "marcus-chen"},
                parent_id=MultiToolCallIdentifier(
                    BlockIdentifier("novel-project.14.mtc.1")
                ),
                generator=Generator.CLAUDE,
                provider_id=ToolProviderIdentifier(
                    BlockIdentifier("summit-root.5.tp-generate")
                ),
            ),
            ToolCall(
                id=ToolCallIdentifier(BlockIdentifier("novel-project.17.tc.6")),
                function_name="generate",
                function_args={"fork": "sophia-patel"},
                parent_id=MultiToolCallIdentifier(
                    BlockIdentifier("novel-project.14.mtc.1")
                ),
                generator=Generator.CLAUDE,
                provider_id=ToolProviderIdentifier(
                    BlockIdentifier("summit-root.5.tp-generate")
                ),
            ),
        ],
        parent_id=ModelResponseIdentifier(
            BlockIdentifier("novel-project.13.mr.3")
        ),
        generator=Generator.CLAUDE,
    )
    MultiToolCallResult(
        id=MultiToolCallResultIdentifier(
            BlockIdentifier("novel-project.18.mtcr.1")
        ),
        tool_call_results=[
            ToolCallResult(
                id=ToolCallResultIdentifier(
                    BlockIdentifier("novel-project.19.tcr.4")
                ),
                tool_call_id=ToolCallIdentifier(
                    BlockIdentifier("novel-project.15.tc.4")
                ),
                text="generated response `elena-blackwood`@`elena-blackwood.7.act.1`",
                result=BlockIdentifier("elena-blackwood.7.act.1"),
                parent_id=BlockIdentifier("novel-project.18.mtcr.1"),
                called_at=datetime.datetime.now(),
                generator=Generator.TOOLS,
            ),
            ToolCallResult(
                id=ToolCallResultIdentifier(
                    BlockIdentifier("novel-project.20.tcr.5")
                ),
                tool_call_id=ToolCallIdentifier(
                    BlockIdentifier("novel-project.16.tc.5")
                ),
                text="generated response `marcus-chen`@`marcus-chen.3.act.1`",
                result=BlockIdentifier("marcus-chen.3.act.1"),
                parent_id=BlockIdentifier("novel-project.18.mtcr.1"),
                called_at=datetime.datetime.now(),
                generator=Generator.TOOLS,
            ),
            ToolCallResult(
                id=ToolCallResultIdentifier(
                    BlockIdentifier("novel-project.21.tcr.6")
                ),
                tool_call_id=ToolCallIdentifier(
                    BlockIdentifier("novel-project.17.tc.6")
                ),
                text="generated response `sophia-patel`@`sophia-patel.3.act.1`",
                result=BlockIdentifier("sophia-patel.3.act.1"),
                parent_id=BlockIdentifier("novel-project.18.mtcr.1"),
                called_at=datetime.datetime.now(),
                generator=Generator.TOOLS,
            ),
        ],
        multi_tool_call_id=MultiToolCallIdentifier(
            BlockIdentifier("novel-project.14.mtc.1")
        ),
        parent_id=BlockIdentifier("novel-project.14.mtc.1"),
        generator=Generator.TOOLS,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("novel-project.22.ui.4")),
        text="apply the 'backstory' label to each of those forks",
        parent_id=BlockIdentifier("novel-project.18.mtcr.1"),
        generator=Generator.USER,
        tool_source_id=None,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("novel-project.23.mr.4")),
        text="I'll apply the backstory label to `elena-blackwood`, `marcus-chen`, and `sophia-patel` forks",
        parent_id=UserInputIdentifier(BlockIdentifier("novel-project.22.ui.4")),
        generator=Generator.CLAUDE,
        temperature=0,
        model="t1",
        max_tokens=64,
    )
    MultiToolCall(
        id=MultiToolCallIdentifier(BlockIdentifier("novel-project.24.mtc.2")),
        tool_calls=[
            ToolCall(
                id=ToolCallIdentifier(BlockIdentifier("novel-project.25.tc.7")),
                function_name="label",
                function_args={"name": "elena-blackwood", "label": "backstory"},
                parent_id=MultiToolCallIdentifier(
                    BlockIdentifier("novel-project.24.mtc.2")
                ),
                generator=Generator.CLAUDE,
                provider_id=ToolProviderIdentifier(
                    BlockIdentifier("summit-root.3.tp-label")
                ),
            ),
            ToolCall(
                id=ToolCallIdentifier(BlockIdentifier("novel-project.26.tc.8")),
                function_name="label",
                function_args={"name": "marcus-chen", "label": "backstory"},
                parent_id=MultiToolCallIdentifier(
                    BlockIdentifier("novel-project.24.mtc.2")
                ),
                generator=Generator.CLAUDE,
                provider_id=ToolProviderIdentifier(
                    BlockIdentifier("summit-root.3.tp-label")
                ),
            ),
            ToolCall(
                id=ToolCallIdentifier(BlockIdentifier("novel-project.27.tc.9")),
                function_name="label",
                function_args={"name": "sophia-patel", "label": "backstory"},
                parent_id=MultiToolCallIdentifier(
                    BlockIdentifier("novel-project.24.mtc.2")
                ),
                generator=Generator.CLAUDE,
                provider_id=ToolProviderIdentifier(
                    BlockIdentifier("summit-root.3.tp-label")
                ),
            ),
        ],
        parent_id=ModelResponseIdentifier(
            BlockIdentifier("novel-project.23.mr.4")
        ),
        generator=Generator.CLAUDE,
    )
    MultiToolCallResult(
        id=MultiToolCallResultIdentifier(
            BlockIdentifier("novel-project.28.mtcr.2")
        ),
        tool_call_results=[
            ToolCallResult(
                id=ToolCallResultIdentifier(
                    BlockIdentifier("novel-project.29.tcr.7")
                ),
                tool_call_id=ToolCallIdentifier(
                    BlockIdentifier("novel-project.25.tc.7")
                ),
                text="applied label 'backstory' to `elena-blackwood`@`elena-blackwood.8.act.2`",
                parent_id=BlockIdentifier("novel-project.28.mtcr.2"),
                result=BlockIdentifier("elena-blackwood.8.act.2"),
                called_at=datetime.datetime.now(),
                generator=Generator.TOOLS,
            ),
            ToolCallResult(
                id=ToolCallResultIdentifier(
                    BlockIdentifier("novel-project.30.tcr.8")
                ),
                tool_call_id=ToolCallIdentifier(
                    BlockIdentifier("novel-project.26.tc.8")
                ),
                text="applied label 'backstory' to `marcus-chen`@`marcus-chen.4.act.2`",
                parent_id=BlockIdentifier("novel-project.28.mtcr.2"),
                result=BlockIdentifier("marcus-chen.4.act.2"),
                called_at=datetime.datetime.now(),
                generator=Generator.TOOLS,
            ),
            ToolCallResult(
                id=ToolCallResultIdentifier(
                    BlockIdentifier("novel-project.31.tcr.9")
                ),
                tool_call_id=ToolCallIdentifier(
                    BlockIdentifier("novel-project.27.tc.9")
                ),
                text="applied label 'backstory' to `sophia-patel`@`sophia-patel.4.act.2`",
                parent_id=BlockIdentifier("novel-project.28.mtcr.2"),
                result=BlockIdentifier("sophia-patel.4.act.2"),
                called_at=datetime.datetime.now(),
                generator=Generator.TOOLS,
            ),
        ],
        multi_tool_call_id=MultiToolCallIdentifier(
            BlockIdentifier("novel-project.24.mtc.2")
        ),
        parent_id=BlockIdentifier("novel-project.24.mtc.2"),
        generator=Generator.TOOLS,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("novel-project.32.ui.5")),
        text="... this is where our example ends, but the conversation has not yet exited ...",
        parent_id=BlockIdentifier("novel-project.28.mtcr.2"),
        generator=Generator.USER,
        tool_source_id=None,
    )
    Branch(
        id=BranchIdentifier(BlockIdentifier("elena-blackwood")),
        labels={"backstory"},
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.6.tcr.0")
        ),
        parent_id=BlockIdentifier("novel-project"),
        generator=Generator.TOOLS,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("elena-blackwood.0.ui.0")),
        text="develop full backstory for 'Elena Blackwood'",
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.6.tcr.0")
        ),
        parent_id=BlockIdentifier("elena-blackwood"),
        generator=Generator.USER,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("elena-blackwood.1.act.0")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.10.tcr.3")
        ),
        description="activated fork `elena-blackwood`. switched from `novel-project`",
        parent_id=BlockIdentifier("elena-blackwood.0.ui.0"),
        generator=Generator.TOOLS,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("elena-blackwood.2.mr.0")),
        text="Elena Blackwood grew up in a Victorian mansion...",
        parent_id=ActivityIdentifier(
            BlockIdentifier("elena-blackwood.1.act.0")
        ),  # proxies through activity to user input
        temperature=0,
        model="t1",
        max_tokens=64,
        generator=Generator.CLAUDE,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("elena-blackwood.3.ui.1")),
        text="thanks, please back out",
        parent_id=BlockIdentifier("elena-blackwood.2.mr.0"),
        tool_source_id=None,
        generator=Generator.USER,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("elena-blackwood.4.mr.1")),
        text="I'll go to the `novel-project` fork",
        parent_id=UserInputIdentifier(
            BlockIdentifier("elena-blackwood.3.ui.1")
        ),
        temperature=0,
        model="t1",
        max_tokens=64,
        generator=Generator.CLAUDE,
    )
    ToolCall(
        id=ToolCallIdentifier(BlockIdentifier("elena-blackwood.5.tc.0")),
        function_name="goto",
        function_args={"name": "novel-project"},
        parent_id=ModelResponseIdentifier(
            BlockIdentifier("elena-blackwood.4.mr.1")
        ),
        provider_id=ToolProviderIdentifier(
            BlockIdentifier("summit-root.0.tp-goto")
        ),
        generator=Generator.CLAUDE,
    )
    ToolCallResult(
        id=ToolCallResultIdentifier(BlockIdentifier("elena-blackwood.6.tcr.0")),
        tool_call_id=ToolCallIdentifier(
            BlockIdentifier("elena-blackwood.5.tc.0")
        ),
        text="activated `novel-project` fork",
        parent_id=BlockIdentifier("elena-blackwood.5.tc.0"),
        called_at=datetime.datetime.now(),
        result=BlockIdentifier("novel-project.11.act.1"),
        generator=Generator.TOOLS,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("elena-blackwood.7.act.1")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.19.tcr.4")
        ),
        description="generate cycle completed",
        parent_id=BlockIdentifier("elena-blackwood.6.tcr.0"),
        generator=Generator.TOOLS,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("elena-blackwood.8.act.2")),
        description="applied label 'backstory'",
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.29.tcr.7")
        ),
        parent_id=BlockIdentifier("elena-blackwood.7.act.1"),
        generator=Generator.TOOLS,
    )
    Branch(
        id=BranchIdentifier(BlockIdentifier("marcus-chen")),
        labels={"backstory"},
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.6.tcr.1")
        ),
        parent_id=BlockIdentifier("novel-project"),
        generator=Generator.TOOLS,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("marcus-chen.0.ui.0")),
        text="develop full backstory for 'Marcus Chen'",
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.6.tc.1")
        ),
        parent_id=BlockIdentifier("marcus-chen"),
        generator=Generator.USER,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("marcus-chen.1.act.0")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.20.tcr.5")
        ),
        description="generate cycle requested",
        parent_id=UserInputIdentifier(BlockIdentifier("marcus-chen.0.ui.0")),
        generator=Generator.TOOLS,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("marcus-chen.2.mr.0")),
        parent_id=ActivityIdentifier(BlockIdentifier("marcus-chen.1.act.0")),
        text="Marcus Chen, a second-generation Chinese-American tech entrepreneur, built his first startup in a San Francisco garage. His parents ran a small electronics repair shop, inspiring his passion for technology. After graduating from Stanford with dual degrees in Computer Science and Electrical Engineering",
        generator=Generator.CLAUDE,
        model="t1",
        temperature=0,
        max_tokens=64,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("marcus-chen.3.act.1")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.20.tcr.5")
        ),
        description="generate cycle completed",
        parent_id=BlockIdentifier("marcus-chen.2.mr.0"),
        generator=Generator.TOOLS,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("marcus-chen.4.act.2")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.30.tcr.8")
        ),
        description="applied label 'backstory'",
        parent_id=BlockIdentifier("marcus-chen.3.act.1"),
        generator=Generator.TOOLS,
    )
    Branch(
        id=BranchIdentifier(BlockIdentifier("sophia-patel")),
        labels={"backstory"},
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.6.tcr.2")
        ),
        parent_id=BlockIdentifier("novel-project"),
        generator=Generator.TOOLS,
    )
    UserInput(
        id=UserInputIdentifier(BlockIdentifier("sophia-patel.0.ui.0")),
        text="develop full backstory for 'Sophia Patel'",
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.6.tcr.2")
        ),
        parent_id=BlockIdentifier("sophia-patel"),
        generator=Generator.USER,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("sophia-patel.1.act.0")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.21.tcr.6")
        ),
        description="generate cycle requested",
        parent_id=UserInputIdentifier(BlockIdentifier("sophia-patel.0.ui.0")),
        generator=Generator.TOOLS,
    )
    ModelResponse(
        id=ModelResponseIdentifier(BlockIdentifier("sophia-patel.2.mr.0")),
        parent_id=ActivityIdentifier(BlockIdentifier("sophia-patel.1.act.0")),
        text="Sophia Patel trained as a classical dancer before becoming a renowned neuroscientist. Born in Mumbai and educated in London, she combines her artistic background with cutting-edge brain research. At 42, she leads a prestigious lab studying movement disorders, inspired by her grandmother's battle with Parkinson's. Her groundbreaking work bridges Eastern meditative practices with Western medical treatments, earning her both acclaim and controversy in academic circles.",
        generator=Generator.CLAUDE,
        model="t1",
        temperature=0,
        max_tokens=64,
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("sophia-patel.3.act.1")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.21.tcr.6")
        ),
        description="generate cycle completed",
        generator=Generator.TOOLS,
        parent_id=BlockIdentifier("sophia-patel.2.mr.0"),
    )
    Activity(
        id=ActivityIdentifier(BlockIdentifier("sophia-patel.4.act.2")),
        tool_source_id=ToolCallResultIdentifier(
            BlockIdentifier("novel-project.31.tcr.9")
        ),
        description="applied label 'backstory'",
        parent_id=BlockIdentifier("sophia-patel.3.act.1"),
        generator=Generator.TOOLS,
    )
