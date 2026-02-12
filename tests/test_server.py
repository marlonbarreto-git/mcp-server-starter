from mcp_starter.models import ToolParam, ToolParamType, ToolCallRequest, Resource
from mcp_starter.server import MCPServer


def test_server_creation():
    server = MCPServer(name="test-server", version="2.0.0")
    assert server.name == "test-server"
    assert server.version == "2.0.0"

    # Test default version
    server_default = MCPServer(name="default")
    assert server_default.version == "1.0.0"


def test_tool_decorator_registers():
    server = MCPServer(name="test")

    @server.tool(name="greet", description="Greet someone", parameters=[
        ToolParam(name="name", type=ToolParamType.STRING, description="Name to greet"),
    ])
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    assert server.registry.tool_exists("greet")
    tool = server.registry.get_tool("greet")
    assert tool.name == "greet"
    assert tool.handler is greet


def test_handle_list_tools():
    server = MCPServer(name="test")

    @server.tool(name="add", description="Add numbers", parameters=[
        ToolParam(name="a", type=ToolParamType.INTEGER, description="First number"),
        ToolParam(name="b", type=ToolParamType.INTEGER, description="Second number"),
    ])
    def add(a: int, b: int) -> int:
        return a + b

    schemas = server.handle_list_tools()
    assert len(schemas) == 1
    assert schemas[0]["name"] == "add"
    assert "inputSchema" in schemas[0]


def test_handle_call_tool_success():
    server = MCPServer(name="test")

    @server.tool(name="add", description="Add numbers")
    def add(a: int, b: int) -> int:
        return a + b

    request = ToolCallRequest(tool_name="add", arguments={"a": 2, "b": 3})
    response = server.handle_call_tool(request)
    assert response.content == "5"
    assert response.is_error is False


def test_handle_call_tool_unknown():
    server = MCPServer(name="test")
    request = ToolCallRequest(tool_name="nonexistent")
    response = server.handle_call_tool(request)
    assert response.is_error is True
    assert "Unknown tool: nonexistent" in response.content


def test_handle_call_tool_error():
    server = MCPServer(name="test")

    @server.tool(name="fail", description="Always fails")
    def fail():
        raise ValueError("Something went wrong")

    request = ToolCallRequest(tool_name="fail")
    response = server.handle_call_tool(request)
    assert response.is_error is True
    assert "Something went wrong" in response.content


def test_handle_list_resources():
    server = MCPServer(name="test")
    resource = Resource(uri="file:///test.txt", name="Test", description="A test file", mime_type="application/json")
    server.registry.register_resource(resource)

    resources = server.handle_list_resources()
    assert len(resources) == 1
    assert resources[0] == {
        "uri": "file:///test.txt",
        "name": "Test",
        "description": "A test file",
        "mimeType": "application/json",
    }
