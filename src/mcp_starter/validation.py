"""Input validation for MCP tool calls."""

from mcp_starter.models import ToolDefinition, ToolParamType


class ValidationError(Exception):
    """Raised when tool call validation fails."""

    def __init__(self, message: str, field: str = ""):
        self.message = message
        self.field = field
        super().__init__(message)


class ToolValidator:
    """Validates tool call arguments against a ToolDefinition."""

    def validate_call(self, tool: ToolDefinition, arguments: dict) -> list[str]:
        errors = []
        # Check required params present
        for param in tool.parameters:
            if param.required and param.name not in arguments:
                errors.append(f"Missing required parameter: {param.name}")
        # Check unknown params
        known_names = {p.name for p in tool.parameters}
        for key in arguments:
            if key not in known_names:
                errors.append(f"Unknown parameter: {key}")
        # Type checking
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
    def _check_type(value, param_type: ToolParamType) -> bool:
        type_map = {
            ToolParamType.STRING: str,
            ToolParamType.INTEGER: int,
            ToolParamType.BOOLEAN: bool,
            ToolParamType.NUMBER: (int, float),
        }
        expected = type_map[param_type]
        # bool is subclass of int in Python, handle specially
        if param_type == ToolParamType.INTEGER and isinstance(value, bool):
            return False
        if param_type == ToolParamType.NUMBER and isinstance(value, bool):
            return False
        return isinstance(value, expected)
