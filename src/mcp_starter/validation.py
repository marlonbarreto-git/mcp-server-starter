"""Input validation for MCP tool calls."""

from typing import Any

from mcp_starter.models import ToolDefinition, ToolParamType

TYPE_MAP: dict[ToolParamType, type | tuple[type, ...]] = {
    ToolParamType.STRING: str,
    ToolParamType.INTEGER: int,
    ToolParamType.BOOLEAN: bool,
    ToolParamType.NUMBER: (int, float),
}


class ValidationError(Exception):
    """Raised when tool call validation fails."""

    def __init__(self, message: str, field: str = "") -> None:
        self.message = message
        self.field = field
        super().__init__(message)


class ToolValidator:
    """Validates tool call arguments against a ToolDefinition."""

    def validate_call(self, tool: ToolDefinition, arguments: dict[str, Any]) -> list[str]:
        """Validate arguments against the tool's parameter definitions.

        Args:
            tool: The tool definition to validate against.
            arguments: Mapping of argument names to values.

        Returns:
            A list of validation error messages (empty if valid).
        """
        errors: list[str] = []
        for param in tool.parameters:
            if param.required and param.name not in arguments:
                errors.append(f"Missing required parameter: {param.name}")
        known_names = {p.name for p in tool.parameters}
        for key in arguments:
            if key not in known_names:
                errors.append(f"Unknown parameter: {key}")
        for param in tool.parameters:
            if param.name in arguments:
                value = arguments[param.name]
                if not self._check_type(value, param.type):
                    errors.append(
                        f"Parameter '{param.name}' expected {param.type.value}, "
                        f"got {type(value).__name__}"
                    )
        return errors

    @staticmethod
    def _check_type(value: Any, param_type: ToolParamType) -> bool:
        expected = TYPE_MAP[param_type]
        if param_type == ToolParamType.INTEGER and isinstance(value, bool):
            return False
        if param_type == ToolParamType.NUMBER and isinstance(value, bool):
            return False
        return isinstance(value, expected)
