from typing import Any

from mcp_starter.models import ToolDefinition, Resource


class MCPRegistry:
    """Central registry for MCP tools and resources."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}
        self._resources: dict[str, Resource] = {}

    def register_tool(self, tool: ToolDefinition) -> None:
        """Add a tool definition to the registry."""
        self._tools[tool.name] = tool

    def register_resource(self, resource: Resource) -> None:
        """Add a resource definition to the registry."""
        self._resources[resource.uri] = resource

    def get_tool(self, name: str) -> ToolDefinition | None:
        """Look up a tool by name, returning None if not found."""
        return self._tools.get(name)

    def get_resource(self, uri: str) -> Resource | None:
        """Look up a resource by URI, returning None if not found."""
        return self._resources.get(uri)

    def list_tools(self) -> list[ToolDefinition]:
        """Return all registered tool definitions."""
        return list(self._tools.values())

    def list_resources(self) -> list[Resource]:
        """Return all registered resource definitions."""
        return list(self._resources.values())

    def tool_exists(self, name: str) -> bool:
        """Check whether a tool with the given name is registered."""
        return name in self._tools

    def to_tool_schemas(self) -> list[dict[str, Any]]:
        """Convert all registered tools to JSON-schema dicts for the MCP protocol."""
        schemas: list[dict[str, Any]] = []
        for tool in self._tools.values():
            properties: dict[str, dict[str, str]] = {}
            required: list[str] = []
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
