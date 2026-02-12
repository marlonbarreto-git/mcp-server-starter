"""JSON-RPC protocol message handling for MCP."""

import json


class ProtocolHandler:
    """Handles JSON-RPC 2.0 message parsing and building."""

    JSONRPC_VERSION = "2.0"

    def parse_request(self, raw: str) -> dict:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        if "method" not in data:
            raise ValueError("Missing 'method' field")
        return data

    def build_response(self, request_id, result) -> str:
        return json.dumps({
            "jsonrpc": self.JSONRPC_VERSION,
            "id": request_id,
            "result": result,
        })

    def build_error(self, request_id, code: int, message: str) -> str:
        return json.dumps({
            "jsonrpc": self.JSONRPC_VERSION,
            "id": request_id,
            "error": {"code": code, "message": message},
        })
