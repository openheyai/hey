"""Tools pipeline for executing tool calls."""

import models
import datetime


def find_tool_provider_block(
    block: models.Block, tool_name: str
) -> models.ToolProviderBlock | None:
    current = block
    while current.parent:
        if (
            isinstance(current, models.ToolProviderBlock)
            and current.name == tool_name
        ):
            return current
        current = current.parent
    return None


def tool_calling_for_single_call(
    block: models.ToolCall,
) -> models.ToolCallResult:
    provider = find_tool_provider_block(block, block.function_name)
    if not provider:
        return models.ToolCallResult(
            parent=block,
            tool_call=block,
            called_at=datetime.datetime.now(),
            finished_at=datetime.datetime.now(),
            error=f"Tool {block.function_name} not found or available to model from this thread",
        )

    result = provider.callable(block, **block.function_args)
    if isinstance(result, models.ToolCallResult):
        return result

    return models.ToolCallResult(
        parent=block,
        tool_call=block,
        called_at=datetime.datetime.now(),
        finished_at=datetime.datetime.now(),
        result=result,
        text=f"Successful result from {provider.name}",
    )


def execute_tool_calls(block: models.Block) -> models.Block:
    if isinstance(block, models.ToolCall):
        return tool_calling_for_single_call(block)
    elif isinstance(block, models.MultiToolCall):
        tool_call_results = [
            tool_calling_for_single_call(tool_call)
            for tool_call in block.tool_calls
        ]
        return models.MultiToolCallResult(
            parent=block, tool_call_results=tool_call_results
        )
    return block


def evaluate(block: models.Block) -> models.Block:
    if not isinstance(block, models.ToolCall) and not isinstance(
        block, models.MultiToolCall
    ):
        return block
    return execute_tool_calls(block)
