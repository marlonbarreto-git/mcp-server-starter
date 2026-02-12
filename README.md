# MCP Server Starter

A template for creating Model Context Protocol (MCP) servers with built-in tool registration, resource handling, and input validation.

## Overview

MCP Server Starter provides a reusable foundation for building MCP-compliant servers that expose tools and resources to LLMs. It handles JSON-RPC 2.0 protocol messaging, tool registration with typed parameters, and argument validation so you can focus on implementing tool logic.

## Architecture

```
┌─────────────────────────────────────────────┐
│               MCPServer                     │
│  ┌────────┐  ┌──────────┐  ┌────────────┐  │
│  │Registry│  │ Protocol │  │ Validation │  │
│  │        │  │ Handler  │  │            │  │
│  │ Tools  │  │ JSON-RPC │  │ Type check │  │
│  │Resources│  │ 2.0      │  │ Required   │  │
│  └────────┘  └──────────┘  └────────────┘  │
└─────────────────────────────────────────────┘
         │              │              │
    register/       parse/build    validate
    lookup          messages       arguments
```

## Features

- Decorator-based tool registration with typed parameters
- JSON-RPC 2.0 request parsing and response building
- Input validation with type checking (string, integer, boolean, number)
- Resource registration and listing
- Automatic JSON Schema generation from tool definitions
- Error handling for unknown tools and invalid arguments

## Tech Stack

- Python 3.11+
- Pydantic >= 2.10

## Quick Start

```bash
git clone https://github.com/marlonbarreto-git/mcp-server-starter.git
cd mcp-server-starter
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Project Structure

```
src/mcp_starter/
  __init__.py
  server.py        # MCPServer with decorator-based tool registration
  models.py        # ToolDefinition, ToolParam, ToolCallRequest/Response, Resource
  protocol.py      # JSON-RPC 2.0 message parsing and building
  registry.py      # MCPRegistry for tools and resources
  validation.py    # ToolValidator with type checking
tests/
  test_server.py
  test_models.py
  test_protocol.py
  test_registry.py
  test_validation.py
```

## Testing

```bash
pytest -v --cov=src/mcp_starter
```

22 tests covering tool registration, protocol parsing, schema generation, input validation, and resource handling.

## License

MIT
