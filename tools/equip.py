import models
import importlib
import inspect

# from functools import partial


def equip(caller: models.Block, function_name: str) -> models.ToolProvider:
    """Load a tool from the project into a ToolProvider.

    Args:
        function_name: Name of the function to load

    Returns:
        [ToolProvider] containing the function if found
        [ExceptionBlock] with error details if there are problems
    """
    if not function_name:
        return models.ExceptionBlock(parent=caller, text="empty function name")

    try:
        module = importlib.import_module(f"tools.{function_name}")
    except ImportError as e:
        return models.ExceptionBlock(parent=caller, text=str(e))

    # Get the function object
    func = getattr(module, function_name, None)
    if not func or not inspect.isfunction(func):
        raise ValueError(f"function {function_name} not declared")

    # # Bind the caller to the function
    # bound_func = partial(func, caller=caller)

    return models.ToolProvider(
        parent=caller,
        name=function_name,
        callable=func
    )
