import models
import datetime
import tools.up
import tools.find_by_type
import tools.find_by_id
import tools.fork
import tools.dump
import tools.load
import tools.label
import tools.generate
import tools.backout
import tools.set


def example_block_tree() -> tuple[models.Root, dict[str, models.Block]]:
    """Creates the example block tree structure from README.md.

    Returns:
        A tuple of (root block, dictionary of all blocks by id)
    """
    root = models.Root(
        id="summit-root",
        parent=None,
        source=models.Generator.TEST,
    )

    # Tool providers
    activate_provider = models.ToolProvider(
        id="sea-turkey",
        parent=root,
        source=models.Generator.TEST,
        name="activate",
        callable=tools.activate.activate,
    )
    root.children = [activate_provider]

    find_provider = models.ToolProvider(
        id="valley-ridge",
        parent=activate_provider,
        source=models.Generator.TEST,
        name="find", 
        callable=tools.find.find
    )
    activate_provider.children = [find_provider]

    fork_provider = models.ToolProvider(
        id="forest-grove",
        parent=find_provider,
        source=models.Generator.TEST,
        name="fork",
        callable=tools.fork.fork,
    )
    find_provider.children = [fork_provider]

    label_provider = models.ToolProvider(
        id="ocean-wave",
        parent=fork_provider,
        source=models.Generator.TEST,
        name="label",
        callable=tools.label.label
    )
    fork_provider.children = [label_provider]

    send_provider = models.ToolProvider(
        id="potato-bath",
        parent=label_provider,
        source=models.Generator.TEST,
        name="send",
        callable=tools.send.send
    )
    label_provider.children = [send_provider]

    generate_provider = models.ToolProvider(
        id="broth-bubble",
        parent=send_provider,
        source=models.Generator.TEST,
        name="generate",
        callable=tools.generate.generate
    )
    send_provider.children = [generate_provider]

    name_provider = models.ToolProvider(
        id="whole-fish",
        parent=generate_provider,
        source=models.Generator.TEST,
        name="name",
        callable=tools.name.name
    )
    generate_provider.children = [name_provider]

    set_provider = models.ToolProvider(
        id="rapid-grey",
        parent=name_provider,
        source=models.Generator.TEST,
        name="set",
        callable=tools.set.set
    )
    name_provider.children = [set_provider]

    backout_provider = models.ToolProvider(
        id="ocean-lake",
        parent=set_provider,
        source=models.Generator.TEST,
        name="backout",
        callable=tools.backout.backout
    )
    set_provider.children = [backout_provider]

    user_input = models.UserInput(
        id="ocean-lake",
        parent=backout_provider,
        source=models.Generator.TEST,
        text="let's fork and write a novel"
    )
    backout_provider.children = [user_input]

    model_response = models.ModelResponse(
        id="forest-path",
        parent=user_input,
        source=models.Generator.TEST,
        text="I'll create a new fork for your novel project. I'll activate it since it seems you want to work on it now.",
        model="test/test-1",
        temperature=0,
        max_tokens=56,
    )
    user_input.children = [model_response]

    tool_call = models.ToolCall(
        id="mountain-trail",
        parent=model_response,
        source=models.Generator.TEST,
        tool_call_id="mountain-trail-id",
        function_name="fork",
        function_args={"name": "novel-project", "activate": True},
        provider=fork_provider,
    )
    model_response.children = [tool_call]

    tool_call_result = models.ToolCallResult(
        id="novel-project",
        parent=tool_call,
        source=models.Generator.TEST,
        tool_call=tool_call,
        called_at=datetime.datetime.now(),
        result="created fork novel-project and set to active",
    )
    tool_call.children = [tool_call_result]

    fork_start = models.Noop(
        id="novel-project",

