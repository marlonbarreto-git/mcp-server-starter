from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ToolParamType(Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    NUMBER = "number"


@dataclass
class ToolParam:
    name: str
    type: ToolParamType
    description: str = ""
    required: bool = True


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: list[ToolParam] = field(default_factory=list)
    handler: Any = None


@dataclass
class ToolCallRequest:
    tool_name: str
    arguments: dict = field(default_factory=dict)


@dataclass
class ToolCallResponse:
    content: str = ""
    is_error: bool = False


@dataclass
class Resource:
    uri: str
    name: str
    description: str = ""
    mime_type: str = "text/plain"
