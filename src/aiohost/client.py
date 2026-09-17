import asyncio
import time
from typing import Any, Literal

import httpx


async def check(
    check_type: Literal["ping", "http", "tcp", "dns", "udp"],
    host: str,
    port: int | None = None,
    max_nodes: int = 3,
    max_wait: float = 30.0,
    poll_interval: float = 1.5,
    nodes: list[str] | None = None,
) -> dict[str, Any]:
    if check_type not in ("ping", "http", "tcp", "dns", "udp"):
        msg = "Invalid check_type"
        raise ValueError(msg)
    if not isinstance(host, str) or not host.strip():
        msg = "Host must be a non-empty string"
        raise ValueError(msg)
    if port is not None and (
        not isinstance(port, int) or not (1 <= port <= 65535)
    ):
        msg = "Port must be an integer between 1 and 65535"
        raise ValueError(msg)
    if max_nodes <= 0:
        msg = "max_nodes must be a positive integer"
        raise ValueError(msg)
    if max_wait <= 0 or poll_interval <= 0:
        msg = "max_wait and poll_interval must be positive"
        raise ValueError()
    if nodes is not None and (
        not isinstance(nodes, list)
        or not all(isinstance(n, str) for n in nodes)
    ):
        msg = "nodes must be a list of strings"
        raise ValueError(msg)

    target = f"{host}:{port}" if port else host
    params: dict[str, Any] = {"host": target, "max_nodes": max_nodes}
    if nodes:
        params["node"] = nodes

    async with httpx.AsyncClient(
        base_url="https://check-host.net",
        headers={"Accept": "application/json"},
        timeout=15.0,
    ) as client:
        resp = await client.get(f"/check-{check_type}", params=params)
        resp.raise_for_status()
        data = resp.json()

        if not data.get("ok"):
            msg = f"API error: {data}"
            raise RuntimeError(msg)

        request_id = data["request_id"]
        start_time = time.monotonic()

        while True:
            await asyncio.sleep(poll_interval)

            res_resp = await client.get(f"/check-result/{request_id}")
            res_resp.raise_for_status()
            result = res_resp.json()

            if (result and not any(v is None for v in result.values())) or (
                time.monotonic() - start_time > max_wait
            ):
                return {"info": data, "result": result}


if __name__ == "__main__":
    import json

    result = asyncio.run(check("ping", "example.com"))
    print(json.dumps(result, indent=2))
