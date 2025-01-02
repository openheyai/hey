import models
import datetime


def forks(caller: models.Block, name: str, user_prompt: str) -> models.Block:
    """List fork names available from this thread. Returns all valid forks
    in a comma delimitted response, or an empty string if there are none."""
    current = caller
    forks = []
    while current.parent:
        if len(current.children) > 1:
            forks += [c.name for c in current.children[1:]]
        current = caller.parent

    result = models.ToolCallResult(
        parent=caller,
        tool_call=caller,
        called_at=datetime.datetime.now(),
        finished_at=datetime.datetime.now(),
        result=forks.join(", "),
    )
    return result
