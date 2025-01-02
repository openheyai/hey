import models
import datetime

import names.friendly_name_generator


def fork(
    caller: models.ToolCall,
    name: str | None,
    user_prompt: str | None,
    activate: bool = False,
) -> models.Block:
    """Forks the conversation, creating a new fork named 'name' that will
    continue the conversation with `user_prompt`.


    The fork becomes a a child of the parent of the last user input. This means
    the fork will _not_ include the message that requests the fork.


    This can be used to pursue multiple conversation options stemming from one
    response"""

    if not name:
        name = names.friendly_name_generator()

    result = models.ToolCallResult(
        id=names.friendly_name_generator(),
        parent=caller,
        tool_call=caller,
        called_at=datetime.datetime.now(),
        finished_at=datetime.datetime.now(),
        result=f"created fork `{name}`",
        source=models.Generator.TOOLS,
    )
    if user_prompt:
        result.result = str(result.result) + " with preset user prompt"
        caller.children.append(
            models.UserInput(
                id=name,
                parent=caller,
                text=user_prompt,
                source=models.Generator.TOOLS,
            )
        )
    else:
        caller.children.append(
            models.Noop(id=name, parent=caller, source=models.Generator.TOOLS)
        )

    if activate:
        result.result = str(result.result) + " and set to active"
        return caller.children[-1]

    return result
