# Terminal-Native-Agent

TerminalNativeAgent is a lightweight, pure-Python AI coding agent designed to run directly in the terminal. It gives an LLM access to a small set of tools so it can inspect files, read and write code, and execute shell commands after user approval.

This project is a practical foundation for building more advanced agentic systems, from local terminal automation to framework-based workflows such as LangChain or other orchestration layers.

## What this project does

- Runs an AI agent in the terminal
- Uses tool calling to perform actions like:
  - listing directories
  - reading files
  - writing files
  - running shell commands
- Keeps the implementation simple and easy to extend
- Demonstrates how a coding agent can work with the local filesystem and command line

## Why this project exists

The goal is to explore the core ideas behind AI agents in a minimal, understandable way before moving to larger frameworks. Instead of relying on a heavy abstraction layer, this project shows the underlying pattern:

- the model receives a prompt
- it decides whether to call a tool
- the tool executes in the local environment
- the result is sent back to the model
- the agent continues or repeat the workflow until it acheive the goal

## Project structure

- `src/agent.py` — main application loop and agent orchestration
- `src/tools.py` — tool implementations
- `src/tools_config.py` — tool schemas exposed to the model
- `.env` — environment variables for the model and API_TOKEN access

## Requirements

- Python 3.14+
- `uv` package manager: curl -LsSf https://astral.sh/uv/install.sh | sh
- An API token for a model provider such as Hugging Face

## Quick start

1. Install dependencies

```bash
uv sync
```

2. Create a `.env` file in the project root with the following values:

```env
HF_TOKEN=your_huggingface_token
MODEL=LLM_URL, e.g Hugging Face
```

3. Run the agent

```bash
uv run ./src/agent.py
```

4. Start chatting in the terminal.

Example:

```text
👨 User: List the project files
```

The agent will decide whether to use a tool and then continue the task.

## Important note

This project can interact with your filesystem and shell. Some actions may modify files or execute commands. Always approve commands before running them when the agent asks for permission.

## Future direction

This repository is meant to be a clean foundation for building more advanced agentic systems. You can extend it with:

- stronger memory and conversation history
- structured tool execution
- better safety checks
- framework integrations such as LangChain or LangGraph
- multi-agent patterns

## License

This project is currently for learning and experimentation.
