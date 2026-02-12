from mcp_starter.models import (
    ToolParamType,
    ToolParam,
    ToolDefinition,
    Resource,
    ToolCallRequest,
    ToolCallResponse,
)


def test_tool_param_type_enum():
    assert ToolParamType.STRING.value == "string"
    assert ToolParamType.INTEGER.value == "integer"
    assert ToolParamType.BOOLEAN.value == "boolean"
    assert ToolParamType.NUMBER.value == "number"


def test_tool_param_creation():
    param = ToolParam(name="query", type=ToolParamType.STRING, description="Search query", required=True)
    assert param.name == "query"
    assert param.type == ToolParamType.STRING
    assert param.description == "Search query"
    assert param.required is True


def test_tool_definition_defaults():
    tool = ToolDefinition(name="search", description="Search tool")
    assert tool.name == "search"
    assert tool.description == "Search tool"
    assert tool.parameters == []
    assert tool.handler is None


def test_resource_creation():
    resource = Resource(uri="file:///tmp/test.txt", name="Test File", description="A test file", mime_type="text/plain")
    assert resource.uri == "file:///tmp/test.txt"
    assert resource.name == "Test File"
    assert resource.description == "A test file"
    assert resource.mime_type == "text/plain"

    # Test defaults
    resource_defaults = Resource(uri="file:///tmp/x.txt", name="X")
    assert resource_defaults.description == ""
    assert resource_defaults.mime_type == "text/plain"


def test_tool_call_request_defaults():
    request = ToolCallRequest(tool_name="search")
    assert request.tool_name == "search"
    assert request.arguments == {}

    request_with_args = ToolCallRequest(tool_name="search", arguments={"query": "hello"})
    assert request_with_args.arguments == {"query": "hello"}


def test_tool_call_response_defaults():
    response = ToolCallResponse(content="result")
    assert response.content == "result"
    assert response.is_error is False

    error_response = ToolCallResponse(content="fail", is_error=True)
    assert error_response.is_error is True
