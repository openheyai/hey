ALL new changes MUST meet ALL of these requirements:

## Structure
1. Models are ONLY in `./models.py`
   - ALL dataclasses MUST be immutable
   - NO methods on models - pure functions only
2. EXACTLY one function per tool file
   - Filename MUST match function name exactly
3. No nested directories; flat file structure preference

## Testing (pytest)
1. NO changes without accompanying tests
2. 100% test coverage - NO EXCEPTIONS
3. NEVER remove existing tests
4. ALL tool tests MUST fit in context
   - If they don't fit, work MUST stop
   - I will block any further changes
5. Requirements MUST be documented in Google-style test docstrings
6. Test source files MUST have suffix with the current date in "YYYYMMDD":
  ./tests/tools/test_dump_json_formatting_20241225.py
7. DO NOT use from import
    BAD:
      from models import ToolCall
    GOOD:
      import models
      value = models.ToolCall(...)

## Code Standards
1. Python 3.12 with COMPLETE type hints
   - NO code without types, including return types
   - NO use of typing.Any
2. Black and Ruff formatting
3. 80 character line limit - NO EXCEPTIONS
4. NO whitespace in blank lines
5. Google python style guide format REQUIRED
6. DO NOT use `typing.Optional` and `typing.Union`
    BAD:
      from typing import Optional, Union
      value: Optional[str]
    GOOD:
      value: str | None

## File System
XDG compliance REQUIRED:
- Config: `~/.config/f5/`
- State: `~/.local/state/f5`
- MUST create if missing

## Process Rules
1. ONE tool modified at a time
   - Multi-tool changes MUST be split into stages
2. DO NOT touch requirements for other toolst
3. NO backwards compatibility
4. Changes MUST be complete, do NOT use placeholders.
Any change not meeting these requirements will be immediately rejected. 

NO EXCEPTIONS!
