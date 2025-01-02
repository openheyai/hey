# f5

wip - framework for llm-based application development

## Core Architecture

### Block Tree
The block tree is the fundamental data structure representing both system state
and capabilities:
- Each block represents a distinct context (development, runtime, authentication, etc.)
- Block position in the tree determines available tools and capabilities
- The tree structure maintains complete system history and state

### Generators
Generators are autonomous agents (LLMs/humans) that evaluate and modify the
block tree:
- Development generators evolve system capabilities by managing tools
- Runtime generators handle application state and user interactions
- Multiple LLMs can act as specialized generators for different contexts

### Tools
Tools are functions that generators can use to modify the block tree:
- Development tools add/remove/update system capabilities
- Runtime tools manage application state and sessions
- Tool availability is contextual based on block position

## Usage

$ python main.py

### Modal Curses

```
── INSERT ─────────────────────────────────────────────────────────────────────
┌─ Context ─────────────────┐ ┌─ Active Forks ─────────────────────────────────┐
│ /                         │ │ elena* (meadow-green)                          │
│ └─ novel                  │ │   └─ elena-birthday                            │
│    ├─ elena*              │ │ marcus (meadow-green)                          │
│    │  └─ elena-birthday   │ │   └─ marcus-birthday                           │
│    ├─ marcus              │ │ sophia (meadow-green)                          │
│    │  └─ marcus-birthday  │ │   └─ sophia-birthday                           │
│    └─ others [+3]         │ │ jackson (meadow-green)                         │
│                           │ │   └─ jackson-birthday                          │
└───────────────────────────┘ └────────────────────────────────────────────────┘
┌─ Messages: 3/27 | Tokens: 182/1247 | Depth: 3 | Variables: birthdays ────────┐
│ [10:42:15] you: tell me Elena's backstory                        stream-bank │
│ [10:42:17] claude: Elena Blackwood grew up in a Victorian        falls-mist  │
│            mansion...                                                        │
│                                                                              │
│ [10:42:19] > back                                                cave-dark   │
│ [10:42:19] ► tool calls (1) | backout                            cliff-edge  │
│   backout() -> success: activated meadow-green                   peak-vista  │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ Recent: meadow-green, elena-blackwood-birthday                               │
└──────────────────────────────────────────────────────────────────────────────┘
/novel/elena > █
```

```
── VISUAL ────────────────────────────────────────────────────────────────────
┌─ Context ─────────────────┐ ┌─ Active Forks ─────────────────────────────────┐
│ /                         │ │ elena* (meadow-green)                          │
│ └─ novel                  │ │   └─ elena-birthday                            │
│    ├─ elena*              │ │ marcus (meadow-green)                          │
│    │  └─ elena-birthday   │ │   └─ marcus-birthday                           │
│    ├─ marcus              │ │ sophia (meadow-green)                          │
│    │  └─ marcus-birthday  │ │   └─ sophia-birthday                           │
│    └─ others [+3]         │ │ jackson (meadow-green)                         │
│                           │ │   └─ jackson-birthday                          │
└───────────────────────────┘ └────────────────────────────────────────────────┘
┌─ Messages: 3/27 | Tokens: 182/1247 | Depth: 3 | Variables: birthdays ────────┐
│ * [10:42:15] > tell me Elena's backstory                         stream-bank │
│                                                                              │
│ * [10:42:17] Claude: Elena Blackwood grew up in a Victorian      falls-mist  │
│            mansion...                                                        │
│                                                                              │
│ * [10:42:19] > back                                              cave-dark   │
│ [10:42:19] ► tool calls (1) | backout                            cliff-edge  │
│   backout() -> success: activated meadow-green                   peak-vista  │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│ Selected: 3 messages | [c]ondense | [d]elete | [e]dit | [y]ank               │
└──────────────────────────────────────────────────────────────────────────────┘
Visual mode (v: toggle selection | j/k: navigate | ESC: command | i: chat)
```

## Contributing
Follow the development rules in ASSISTANTS.md and ensure all changes have associated tests.
