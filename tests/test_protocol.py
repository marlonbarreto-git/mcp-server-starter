"""Tests for JSON-RPC protocol message handling."""

import json

import pytest

from mcp_starter.protocol import ProtocolHandler


@pytest.fixture
def handler():
    return ProtocolHandler()


class TestProtocolHandler:
    def test_parse_valid_request(self, handler):
        raw = json.dumps({"jsonrpc": "2.0", "method": "tools/call", "id": 1})
        result = handler.parse_request(raw)
        assert result["method"] == "tools/call"
        assert result["id"] == 1

    def test_parse_invalid_json(self, handler):
        with pytest.raises(ValueError, match="Invalid JSON"):
            handler.parse_request("not json {{{")

    def test_parse_missing_method(self, handler):
        raw = json.dumps({"jsonrpc": "2.0", "id": 1})
        with pytest.raises(ValueError, match="Missing 'method' field"):
            handler.parse_request(raw)

    def test_build_response(self, handler):
        response = handler.build_response(request_id=1, result={"ok": True})
        parsed = json.loads(response)
        assert parsed["jsonrpc"] == "2.0"
        assert parsed["id"] == 1
        assert parsed["result"] == {"ok": True}

    def test_build_error(self, handler):
        response = handler.build_error(request_id=2, code=-32600, message="Invalid Request")
        parsed = json.loads(response)
        assert parsed["jsonrpc"] == "2.0"
        assert parsed["id"] == 2
        assert parsed["error"]["code"] == -32600
        assert parsed["error"]["message"] == "Invalid Request"

    def test_jsonrpc_version(self, handler):
        assert handler.JSONRPC_VERSION == "2.0"
