"""MCP Server Starter - Template for MCP servers."""

__all__ = [
    "MCPRegistry",
    "MCPServer",
    "ProtocolHandler",
    "Resource",
    "ToolCallRequest",
    "ToolCallResponse",
    "ToolDefinition",
    "ToolParam",
    "ToolParamType",
    "ToolValidator",
    "ValidationError",
]

__version__ = "0.1.0"

from .models import Resource, ToolCallRequest, ToolCallResponse, ToolDefinition, ToolParam, ToolParamType
from .protocol import ProtocolHandler
from .registry import MCPRegistry
from .server import MCPServer
from .validation import ToolValidator, ValidationError
