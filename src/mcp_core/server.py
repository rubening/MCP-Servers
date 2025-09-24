from __future__ import annotations

import inspect
import logging
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict

JsonDict = Dict[str, Any]
ToolHandler = Callable[[JsonDict], Awaitable[JsonDict] | JsonDict]


class MCPError(Exception):
    """User-facing error with a specific JSON-RPC code."""

    def __init__(self, message: str, *, code: int = -32000, data: Any | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.data = data


@dataclass(slots=True)
class ToolSpec:
    """Describes an MCP tool and its handler."""

    name: str
    description: str
    input_schema: JsonDict
    handler: ToolHandler
    metadata: JsonDict | None = field(default=None)

    def to_json(self) -> JsonDict:
        payload: JsonDict = {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }
        if self.metadata:
            payload.update(self.metadata)
        return payload


class BaseMCPServer:
    """Shared JSON-RPC 2.0 handler for MCP servers."""

    def __init__(
        self,
        name: str,
        version: str,
        *,
        protocol_version: str = "2024-11-05",
        logger: logging.Logger | None = None,
    ) -> None:
        self.name = name
        self.version = version
        self.protocol_version = protocol_version
        self._tools: Dict[str, ToolSpec] = {}
        self.logger = logger or logging.getLogger(name)

    # ------------------------------------------------------------------
    # Tool registration
    # ------------------------------------------------------------------
    def register_tool(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"Tool '{spec.name}' already registered")
        self._tools[spec.name] = spec
        self.logger.debug("Registered tool %s", spec.name)

    def tools_payload(self) -> JsonDict:
        return {"tools": [spec.to_json() for spec in self._tools.values()]}

    # ------------------------------------------------------------------
    # JSON-RPC helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _request_id(request: JsonDict) -> Any:
        req_id = request.get("id")
        return 0 if req_id is None else req_id

    def _success(self, request_id: Any, result: JsonDict) -> JsonDict:
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    def _error(
        self,
        request_id: Any,
        message: str,
        *,
        code: int = -32000,
        data: Any | None = None,
    ) -> JsonDict:
        error: JsonDict = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        return {"jsonrpc": "2.0", "id": request_id, "error": error}

    async def _maybe_await(self, handler: ToolHandler, arguments: JsonDict) -> JsonDict:
        try:
            result = handler(arguments)
            if inspect.isawaitable(result):
                result = await result  # type: ignore[assignment]
        except MCPError:
            raise
        except Exception as exc:  # pragma: no cover - surfaced to caller
            self.logger.exception(
                "Tool execution failed: %s", getattr(handler, "__name__", handler)
            )
            raise exc

        if not isinstance(result, dict):
            raise TypeError(
                f"Tool '{getattr(handler, '__name__', handler)}' returned non-dict payload: {type(result).__name__}"
            )
        return result

    # ------------------------------------------------------------------
    # JSON-RPC request handling
    # ------------------------------------------------------------------
    async def handle_request(self, request: JsonDict) -> JsonDict:
        method = request.get("method", "")
        request_id = self._request_id(request)

        try:
            if method == "initialize":
                return self._success(
                    request_id,
                    {
                        "protocolVersion": self.protocol_version,
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": self.name, "version": self.version},
                    },
                )

            if method == "tools/list":
                return self._success(request_id, self.tools_payload())

            if method == "tools/call":
                params = request.get("params") or {}
                name = params.get("name")
                if not name:
                    raise MCPError("Missing tool name", code=-32602)

                tool = self._tools.get(name)
                if not tool:
                    raise MCPError(f"Unknown tool '{name}'", code=-32601)

                arguments = params.get("arguments") or {}
                if not isinstance(arguments, dict):
                    raise MCPError("Tool arguments must be an object", code=-32602)

                result = await self._maybe_await(tool.handler, arguments)
                return self._success(request_id, result)

            raise MCPError(f"Unsupported method '{method}'", code=-32601)

        except MCPError as exc:
            self.logger.info("User error: %s", exc)
            return self._error(request_id, str(exc), code=exc.code, data=exc.data)
        except Exception as exc:
            self.logger.exception("Unhandled server error")
            return self._error(request_id, str(exc))
