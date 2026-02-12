from mcp_starter.models import ToolDefinition, ToolParam, ToolCallRequest, ToolCallResponse
from mcp_starter.registry import MCPRegistry


class MCPServer:
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.registry = MCPRegistry()

    def tool(self, name: str, description: str, parameters: list[ToolParam] | None = None):
        def decorator(func):
            tool_def = ToolDefinition(
                name=name,
                description=description,
                parameters=parameters or [],
                handler=func,
            )
            self.registry.register_tool(tool_def)
            return func
        return decorator

    def handle_list_tools(self) -> list[dict]:
        return self.registry.to_tool_schemas()

    def handle_call_tool(self, request: ToolCallRequest) -> ToolCallResponse:
        tool = self.registry.get_tool(request.tool_name)
        if tool is None:
            return ToolCallResponse(content=f"Unknown tool: {request.tool_name}", is_error=True)
        try:
            result = tool.handler(**request.arguments)
            return ToolCallResponse(content=str(result))
        except Exception as e:
            return ToolCallResponse(content=f"Error: {e}", is_error=True)

    def handle_list_resources(self) -> list[dict]:
        return [
            {
                "uri": r.uri,
                "name": r.name,
                "description": r.description,
                "mimeType": r.mime_type,
            }
            for r in self.registry.list_resources()
        ]
