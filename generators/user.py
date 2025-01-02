"""User pipeline for handling user interactions."""

import models


def thread_name(block: models.Block) -> str:
    ancestor_count = 0
    ancestor_forks = []
    current = block

    while True:
        if isinstance(current, models.RootBlock):
            ancestor_forks.append(f"{current.nick}")
            break

        ancestor_count += 1
        parent = current.parent

        if len(parent.children) > 0:
            try:
                index = parent.children.index(current)
            except ValueError:
                index = -1
            ancestor_forks.append(f"{parent.nick}[{index}]")

        current = parent

    return ">".join(reversed(ancestor_forks))


def evaluate(block: models.Block) -> models.Block:
    if isinstance(block, models.UserInput):
        return block

    prompt_thread_mark = "[" + thread_name(block) + "] "

    if isinstance(block, models.ToolCall):
        print(
            prompt_thread_mark + "tool call: ",
            block.function_name,
            block.function_args,
        )
        return block

    if isinstance(block, models.MultiToolCall):
        for tool_call in block.tool_calls:
            print(
                prompt_thread_mark + "tool call: ",
                tool_call.function_name,
                tool_call.function_args,
            )
        return block

    if isinstance(block, models.ToolCallResult):
        print(prompt_thread_mark + " tool call result")
        return block

    if isinstance(block, models.MultiToolCallResult):
        print(prompt_thread_mark + " tool call result")
        return block

    if isinstance(block, models.ExceptionBlock):
        print(prompt_thread_mark + " exception:", block.text)

    if isinstance(block, models.ModelResponse):
        print(prompt_thread_mark + block.model + ": " + block.text)

    return models.UserInput(
        parent=block, text=input(prompt_thread_mark + "user: ")
    )
