from typing import Any, Callable

from mcp_starter.models import ToolDefinition, ToolParam, ToolCallRequest, ToolCallResponse
from mcp_starter.registry import MCPRegistry

DEFAULT_VERSION = "1.0.0"


class MCPServer:
    """Top-level MCP server that registers tools/resources and dispatches requests."""

    def __init__(self, name: str, version: str = DEFAULT_VERSION) -> None:
        self.name = name
        self.version = version
        self.registry = MCPRegistry()

    def tool(
        self, name: str, description: str, parameters: list[ToolParam] | None = None
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator that registers a function as an MCP tool.

        Args:
            name: Unique tool name exposed to clients.
            description: Human-readable description of the tool.
            parameters: Optional list of parameter definitions.

        Returns:
            A decorator that registers the wrapped function.
        """
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            tool_def = ToolDefinition(
                name=name,
                description=description,
                parameters=parameters or [],
                handler=func,
            )
            self.registry.register_tool(tool_def)
            return func
        return decorator

    def handle_list_tools(self) -> list[dict[str, Any]]:
        """Return JSON-schema representations of all registered tools."""
        return self.registry.to_tool_schemas()

    def handle_call_tool(self, request: ToolCallRequest) -> ToolCallResponse:
        """Execute a tool by name with the provided arguments.

        Args:
            request: The incoming tool call request.

        Returns:
            A response containing the result or an error message.
        """
        tool = self.registry.get_tool(request.tool_name)
        if tool is None:
            return ToolCallResponse(content=f"Unknown tool: {request.tool_name}", is_error=True)
        try:
            result = tool.handler(**request.arguments)
            return ToolCallResponse(content=str(result))
        except Exception as e:
            return ToolCallResponse(content=f"Error: {e}", is_error=True)

    def handle_list_resources(self) -> list[dict[str, str]]:
        """Return serialized representations of all registered resources."""
        return [
            {
                "uri": r.uri,
                "name": r.name,
                "description": r.description,
                "mimeType": r.mime_type,
            }
            for r in self.registry.list_resources()
        ]
