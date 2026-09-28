#!/usr/bin/env python3
"""Minimal stdio MCP client for Konnect."""
from __future__ import annotations

import json
import os
import select
import subprocess
import sys
import time
from typing import Any


class Konnect:
    def __init__(self, config: str = "/workspace/konnect.toml") -> None:
        env = os.environ.copy()
        env["RUST_LOG"] = "warn"
        self.p = subprocess.Popen(
            ["/workspace/tools/konnect/konnect", "--config", config],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )
        self._id = 0
        self.initialize()

    def _send(self, obj: dict[str, Any]) -> None:
        assert self.p.stdin is not None
        self.p.stdin.write(json.dumps(obj) + "\n")
        self.p.stdin.flush()

    def _read(self, timeout: float = 30.0) -> dict[str, Any] | None:
        assert self.p.stdout is not None
        end = time.time() + timeout
        while time.time() < end:
            r, _, _ = select.select([self.p.stdout], [], [], 0.2)
            if not r:
                continue
            line = self.p.stdout.readline()
            if not line:
                return None
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
        return None

    def call(self, method: str, params: dict[str, Any] | None = None, timeout: float = 60.0) -> Any:
        self._id += 1
        req_id = self._id
        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            payload["params"] = params
        self._send(payload)
        end = time.time() + timeout
        while time.time() < end:
            msg = self._read(timeout=end - time.time())
            if msg is None:
                break
            if msg.get("method") and "id" not in msg:
                # notification
                continue
            if msg.get("id") == req_id:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result")
        raise TimeoutError(f"timeout waiting for {method}")

    def tool(self, name: str, arguments: dict[str, Any] | None = None, timeout: float = 60.0) -> Any:
        result = self.call(
            "tools/call",
            {"name": name, "arguments": arguments or {}},
            timeout=timeout,
        )
        content = result.get("content", [])
        texts = []
        for item in content:
            if item.get("type") == "text":
                texts.append(item.get("text", ""))
        joined = "\n".join(texts)
        try:
            return json.loads(joined)
        except Exception:
            if result.get("isError"):
                raise RuntimeError(joined or result)
            return joined or result

    def initialize(self) -> None:
        self.call(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "voz9-agent", "version": "1.0"},
            },
        )
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def close(self) -> None:
        self.p.terminate()
        try:
            self.p.wait(timeout=3)
        except Exception:
            self.p.kill()


def main() -> None:
    k = Konnect()
    try:
        for ts in [
            "sch_components",
            "sch_wiring",
            "sch_analysis",
            "sch_export",
            "sch_hierarchy",
            "sch_batch",
        ]:
            print("load", ts, k.tool("load_toolset", {"name": ts}))
        tools = k.call("tools/list", {})
        names = sorted(t["name"] for t in tools["tools"])
        print("total", len(names))
        for n in names:
            print(n)
        for t in tools["tools"]:
            if t["name"] in {
                "add_symbol",
                "place_symbol",
                "add_component",
                "add_power_symbol",
                "add_wire",
                "add_label",
                "add_global_label",
                "open_project",
                "get_project_info",
                "create_schematic",
                "list_symbols",
                "search_symbols",
            } or "power" in t["name"] or "symbol" in t["name"]:
                print("\n===", t["name"], "===")
                print(json.dumps(t.get("inputSchema", {}), indent=2)[:2000])
    finally:
        k.close()


if __name__ == "__main__":
    main()
