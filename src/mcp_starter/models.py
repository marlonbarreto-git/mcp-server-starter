from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

DEFAULT_MIME_TYPE = "text/plain"


class ToolParamType(Enum):
    """Supported JSON Schema types for tool parameters."""

    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    NUMBER = "number"


@dataclass
class ToolParam:
    """Definition of a single parameter accepted by a tool."""

    name: str
    type: ToolParamType
    description: str = ""
    required: bool = True


@dataclass
class ToolDefinition:
    """Complete definition of a tool including its handler function."""

    name: str
    description: str
    parameters: list[ToolParam] = field(default_factory=list)
    handler: Callable[..., Any] | None = None


@dataclass
class ToolCallRequest:
    """Incoming request to invoke a specific tool with arguments."""

    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolCallResponse:
    """Result returned after executing a tool call."""

    content: str = ""
    is_error: bool = False


@dataclass
class Resource:
    """An MCP resource exposed to clients."""

    uri: str
    name: str
    description: str = ""
    mime_type: str = DEFAULT_MIME_TYPE
