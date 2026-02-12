"""Tests for input validation of tool calls."""

import pytest

from mcp_starter.models import ToolDefinition, ToolParam, ToolParamType
from mcp_starter.validation import ToolValidator


@pytest.fixture
def validator():
    return ToolValidator()


@pytest.fixture
def sample_tool():
    return ToolDefinition(
        name="greet",
        description="Greet a user",
        parameters=[
            ToolParam(name="name", type=ToolParamType.STRING, required=True),
            ToolParam(name="age", type=ToolParamType.INTEGER, required=True),
            ToolParam(name="verbose", type=ToolParamType.BOOLEAN, required=False),
        ],
    )


class TestToolValidator:
    def test_valid_call_no_errors(self, validator, sample_tool):
        errors = validator.validate_call(sample_tool, {"name": "Alice", "age": 30})
        assert errors == []

    def test_missing_required_param(self, validator, sample_tool):
        errors = validator.validate_call(sample_tool, {"name": "Alice"})
        assert len(errors) == 1
        assert "Missing required parameter: age" in errors[0]

    def test_unknown_param(self, validator, sample_tool):
        errors = validator.validate_call(
            sample_tool, {"name": "Alice", "age": 30, "color": "blue"}
        )
        assert len(errors) == 1
        assert "Unknown parameter: color" in errors[0]

    def test_wrong_type_string(self, validator, sample_tool):
        errors = validator.validate_call(sample_tool, {"name": 123, "age": 30})
        assert len(errors) == 1
        assert "expected string" in errors[0]

    def test_wrong_type_integer(self, validator, sample_tool):
        errors = validator.validate_call(sample_tool, {"name": "Alice", "age": "thirty"})
        assert len(errors) == 1
        assert "expected integer" in errors[0]

    def test_bool_not_integer(self, validator, sample_tool):
        """bool is a subclass of int in Python, but should NOT pass as integer."""
        errors = validator.validate_call(
            sample_tool, {"name": "Alice", "age": True}
        )
        assert len(errors) == 1
        assert "expected integer" in errors[0]

    def test_number_accepts_int_and_float(self, validator):
        tool = ToolDefinition(
            name="calc",
            description="Calculate",
            parameters=[
                ToolParam(name="value", type=ToolParamType.NUMBER, required=True),
            ],
        )
        assert validator.validate_call(tool, {"value": 42}) == []
        assert validator.validate_call(tool, {"value": 3.14}) == []

    def test_optional_param_missing_ok(self, validator, sample_tool):
        # "verbose" is optional, omitting it should produce no errors
        errors = validator.validate_call(sample_tool, {"name": "Alice", "age": 25})
        assert errors == []

    def test_multiple_errors(self, validator, sample_tool):
        # Missing "age" (required) + wrong type for "name"
        errors = validator.validate_call(sample_tool, {"name": 999})
        assert len(errors) == 2
        assert any("Missing required parameter: age" in e for e in errors)
        assert any("expected string" in e for e in errors)
