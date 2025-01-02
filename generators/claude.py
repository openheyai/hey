from models import (
    Block,
    ExceptionBlock,
    ToolProviderBlock,
    UserInput,
    ModelResponse,
    RootBlock,
    ToolCallResult,
    MultiToolCall,
    ToolCall,
    MultiToolCallResult,
)
from typing import Any
import os
from anthropic import Anthropic

from typing import Callable, Dict
import inspect

import re


def _parse_docstring(func: Callable) -> tuple[str, Dict[str, Any]]:
    """Parse a docstring to extract function and parameter descriptions.

    Validates that the docstring contains sufficient documentation including examples.

    Args:
        func: The function whose docstring should be parsed

    Returns:
        A tuple containing (function description, parameter descriptions)
    """
    doc = inspect.getdoc(func)
    #
    # if not doc:
    #     raise InsufficientDocumentationError(
    #         f"ToolProviderBlock {func.__name__} is missing a docstring"
    #     )
    #
    # # Check for minimum length
    # if len(doc) < 50:  # Arbitrary minimum length for a substantive docstring
    #     raise InsufficientDocumentationError(
    #         f"Docstring for {func.__name__} is too brief (less than 50 chars)"
    #     )
    #
    # # Check for examples section
    # if 'example' not in doc.lower():
    #     raise InsufficientDocumentationError(
    #         f"Docstring for {func.__name__} must include at least one example"
    #     )

    lines = [line.strip() for line in doc.split("\n")]
    func_desc = []
    param_desc = {}
    in_params = False

    for line in lines:
        if not line:
            continue
        if line.lower().startswith(("args:", "arguments:", "parameters:")):
            in_params = True
            continue
        if in_params:
            match = re.match(r"(\w+):\s*(.+)", line)
            if match:
                param_desc[match.group(1)] = match.group(2)
            elif line.lower().startswith(("returns:", "raises:")):
                break
        else:
            func_desc.append(line)

    return " ".join(func_desc), param_desc


def _claude_tool_spec_for(func: Callable) -> Dict[str, Any]:
    """Generate a Claude-compatible tool specification from a Python function.

    Args:
        func: The function to create a tool specification for

    Returns:
        A dictionary containing the tool specification in Claude's format
    """
    # Handle partial functions
    # if isinstance(func, partial):
    #     name = func.func.__name__
    #     sig = inspect.signature(func.func)
    #     # Remove the first parameter which is handled by partial
    #     parameters = list(sig.parameters.items())[1:]
    #     description, param_descriptions = _parse_docstring(func.func)
    # else:
    name = func.__name__
    sig = inspect.signature(func)
    parameters = list(sig.parameters.items())[1:]
    description, param_descriptions = _parse_docstring(func)

    # Build parameters list
    required = []
    properties = {}

    for param_name, param in parameters:
        # param_type = param.annotation if param.annotation != inspect._empty else Any
        param_desc = param_descriptions.get(param_name, "")

        if param.default == inspect._empty:
            required.append(param_name)

        properties[param_name] = {
            "type": "string",  # Simplify all types to string for Claude
            "description": param_desc,
        }

    # Return in Claude's expected format with input_schema
    return {
        "name": name,
        "description": description,
        "input_schema": {  # Added input_schema as required by Claude API
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }


def evaluate(
    block: Block,
    model: str = "claude-3-5-haiku-20241022",
    temperature: float = 0,
    max_tokens: int = 2048,
    tool_choice: str = "auto",
) -> Block:
    # this generator only creates blocks in response to user input or completed tool calls
    if (
        not isinstance(block, UserInput)
        and not isinstance(block, ToolCallResult)
        and not isinstance(block, MultiToolCallResult)
    ):
        return block

    messages: list[dict] = []
    tools = {}

    current = block
    while current and not isinstance(current, RootBlock):
        if isinstance(current, UserInput):
            messages.append({"role": "user", "content": current.text})
        elif isinstance(current, ToolProviderBlock):
            tools[current.name] = _claude_tool_spec_for(current.callable)
        elif isinstance(current, ModelResponse):
            message = {"role": "assistant", "content": []}
            if current.text:
                message["content"].append(
                    {"type": "text", "text": current.text}
                )

            if current.tool_calls:
                message["content"] += [
                    {
                        "id": tool_call.tool_call_id,
                        "type": "tool_use",
                        "name": tool_call.function_name,
                        "input": tool_call.function_args,
                    }
                    for tool_call in current.tool_calls
                ]
            messages.append(message)
        elif isinstance(current, ToolCallResult):
            message = {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": current.tool_call.tool_call_id,
                        "content": (current.result or current.error),
                    }
                ],
            }
            if current.error:
                message["content"][0]["is_error"] = True

            messages.append(message)
        elif isinstance(current, MultiToolCallResult):
            message = {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_call_result.tool_call.tool_call_id,
                        "content": (
                            tool_call_result.result or tool_call_result.error
                        ),
                    }
                    for tool_call_result in current.tool_call_results
                ],
            }
            messages.append(message)

        current = current.parent

    completion_args = {
        "model": model,
        "messages": list(reversed(messages)),
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if tools:
        completion_args["tools"] = list(tools.values())
        if tool_choice in ("auto", "any"):
            completion_args["tool_choice"] = {"type": tool_choice}
        else:
            completion_args["tool_choice"] = {
                "type": "tool",
                "name": tool_choice,
            }

    from pprint import pp

    pp(completion_args)

    try:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(**completion_args)
    except Exception as e:
        return ExceptionBlock(
            parent=block, text=f"Claude completion error: {e}"
        )

    if not response:
        return ExceptionBlock(parent=block, text="No response")

    text_response = ""
    tool_calls = []

    for part in response.content:
        if part.type == "text":
            text_response += part.text
        elif part.type == "tool_use":
            tool_calls.append(
                ToolCall(
                    parent=None,  # set below
                    tool_call_id=part.id,
                    function_name=part.name,
                    function_args=part.input,
                    type=part.type,
                )
            )

    model_response = ModelResponse(
        parent=block,
        text=text_response,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        tool_calls=tool_calls,
    )

    if tool_calls:
        if len(tool_calls) == 1:
            tool_calls[0].parent = model_response
            return tool_calls[0]
        else:
            multi_tool_call = MultiToolCall(
                parent=model_response, tool_calls=tool_calls
            )
            for tool_call in tool_calls:
                tool_call.parent = multi_tool_call
            return multi_tool_call
    else:
        return model_response
