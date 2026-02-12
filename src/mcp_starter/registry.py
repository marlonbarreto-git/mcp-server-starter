from mcp_starter.models import ToolDefinition, Resource


class MCPRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}
        self._resources: dict[str, Resource] = {}

    def register_tool(self, tool: ToolDefinition) -> None:
        self._tools[tool.name] = tool

    def register_resource(self, resource: Resource) -> None:
        self._resources[resource.uri] = resource

    def get_tool(self, name: str) -> ToolDefinition | None:
        return self._tools.get(name)

    def get_resource(self, uri: str) -> Resource | None:
        return self._resources.get(uri)

    def list_tools(self) -> list[ToolDefinition]:
        return list(self._tools.values())

    def list_resources(self) -> list[Resource]:
        return list(self._resources.values())

    def tool_exists(self, name: str) -> bool:
        return name in self._tools

    def to_tool_schemas(self) -> list[dict]:
        schemas = []
        for tool in self._tools.values():
            properties = {}
            required = []
            for p in tool.parameters:
                properties[p.name] = {"type": p.type.value, "description": p.description}
                if p.required:
                    required.append(p.name)
            schemas.append({
                "name": tool.name,
                "description": tool.description,
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            })
        return schemas
