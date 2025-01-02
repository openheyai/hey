import models
import datetime
import tools.up


def up_tool_call_result() -> (
    tuple[models.ToolCallResult, dict[str, models.Block]]
):
    """Creates a test block tree structure.

    Returns:
        A ToolCallResult block with expected ancestry
    """
    root = models.Root(
        id="root",
        parent=None,
        source=models.Generator.TEST,
    )

    tool_provider = models.ToolProvider(
        id="toolprovider1",
        parent=root,
        source=models.Generator.TEST,
        name="identity",
        callable=tools.up.up,
    )
    root.children = [tool_provider]

    user_input = models.UserInput(
        id="user1",
        text="input 1",
        parent=tool_provider,
        source=models.Generator.TEST,
    )
    tool_provider.children = [user_input]

    model_response = models.ModelResponse(
        id="model1",
        parent=user_input,
        source=models.Generator.TEST,
        text="will call the up tool",
        model="test/test-1",
        temperature=0,
        max_tokens=56,
    )
    user_input.children = [model_response]

    tool_call = models.ToolCall(
        id="tool1",
        parent=model_response,
        source=models.Generator.TEST,
        tool_call_id="tool1_id",
        function_name="up",
        function_args=dict(),
        provider=tool_provider,
    )
    model_response.children = [tool_call]

    result = models.ToolCallResult(
        id="result1",
        parent=tool_call,
        source=models.Generator.TEST,
        tool_call=tool_call,
        called_at=datetime.datetime.now(),
        result=user_input,
    )
    tool_call.children = [result]

    return result, {
        root.id: root,
        tool_provider.id: tool_provider,
        user_input.id: user_input,
        model_response.id: model_response,
        tool_call.id: tool_call,
        result.id: result,
    }
