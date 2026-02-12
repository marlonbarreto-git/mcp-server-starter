"""JSON-RPC protocol message handling for MCP."""

import json
from typing import Any


class ProtocolHandler:
    """Handles JSON-RPC 2.0 message parsing and building."""

    JSONRPC_VERSION = "2.0"

    def parse_request(self, raw: str) -> dict[str, Any]:
        """Parse a raw JSON-RPC request string into a dict.

        Args:
            raw: JSON-encoded request string.

        Returns:
            Parsed request as a dictionary.

        Raises:
            ValueError: If the JSON is malformed or missing required fields.
        """
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        if "method" not in data:
            raise ValueError("Missing 'method' field")
        return data

    def build_response(self, request_id: Any, result: Any) -> str:
        """Build a JSON-RPC success response string.

        Args:
            request_id: The id from the original request.
            result: The result payload to include.

        Returns:
            JSON-encoded response string.
        """
        return json.dumps({
            "jsonrpc": self.JSONRPC_VERSION,
            "id": request_id,
            "result": result,
        })

    def build_error(self, request_id: Any, code: int, message: str) -> str:
        """Build a JSON-RPC error response string.

        Args:
            request_id: The id from the original request.
            code: JSON-RPC error code.
            message: Human-readable error description.

        Returns:
            JSON-encoded error response string.
        """
        return json.dumps({
            "jsonrpc": self.JSONRPC_VERSION,
            "id": request_id,
            "error": {"code": code, "message": message},
        })
