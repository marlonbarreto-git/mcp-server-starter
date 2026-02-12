from mcp_starter.models import ToolDefinition, ToolParam, ToolParamType, Resource
from mcp_starter.registry import MCPRegistry


def test_register_and_get_tool():
    registry = MCPRegistry()
    tool = ToolDefinition(name="search", description="Search tool")
    registry.register_tool(tool)
    result = registry.get_tool("search")
    assert result is tool


def test_register_and_get_resource():
    registry = MCPRegistry()
    resource = Resource(uri="file:///test.txt", name="Test")
    registry.register_resource(resource)
    result = registry.get_resource("file:///test.txt")
    assert result is resource


def test_get_nonexistent_tool_returns_none():
    registry = MCPRegistry()
    assert registry.get_tool("nonexistent") is None


def test_get_nonexistent_resource_returns_none():
    registry = MCPRegistry()
    assert registry.get_resource("nonexistent") is None


def test_list_tools_returns_all():
    registry = MCPRegistry()
    t1 = ToolDefinition(name="tool1", description="First")
    t2 = ToolDefinition(name="tool2", description="Second")
    registry.register_tool(t1)
    registry.register_tool(t2)
    tools = registry.list_tools()
    assert len(tools) == 2
    assert t1 in tools
    assert t2 in tools


def test_list_resources_returns_all():
    registry = MCPRegistry()
    r1 = Resource(uri="file:///a.txt", name="A")
    r2 = Resource(uri="file:///b.txt", name="B")
    registry.register_resource(r1)
    registry.register_resource(r2)
    resources = registry.list_resources()
    assert len(resources) == 2
    assert r1 in resources
    assert r2 in resources


def test_tool_exists_true():
    registry = MCPRegistry()
    registry.register_tool(ToolDefinition(name="search", description="Search"))
    assert registry.tool_exists("search") is True


def test_tool_exists_false():
    registry = MCPRegistry()
    assert registry.tool_exists("search") is False


def test_to_tool_schemas_format():
    registry = MCPRegistry()
    tool = ToolDefinition(
        name="search",
        description="Search the web",
        parameters=[
            ToolParam(name="query", type=ToolParamType.STRING, description="Search query", required=True),
            ToolParam(name="limit", type=ToolParamType.INTEGER, description="Max results", required=False),
        ],
    )
    registry.register_tool(tool)
    schemas = registry.to_tool_schemas()

    assert len(schemas) == 1
    schema = schemas[0]
    assert schema["name"] == "search"
    assert schema["description"] == "Search the web"
    assert schema["inputSchema"]["type"] == "object"
    assert "query" in schema["inputSchema"]["properties"]
    assert schema["inputSchema"]["properties"]["query"] == {
        "type": "string",
        "description": "Search query",
    }
    assert schema["inputSchema"]["properties"]["limit"] == {
        "type": "integer",
        "description": "Max results",
    }
    assert schema["inputSchema"]["required"] == ["query"]
