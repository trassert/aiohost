# Aiohost

<p align="center">
<a href=https://t.me/lumintoch><img src=https://img.shields.io/badge/Sponsored%20by-Luminto-purple?style=for-the-badge&logo=githubsponsors&logoColor=white></a>
<img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white" alt="Badge">
<img src="https://img.shields.io/badge/Ruff-FFC131?style=for-the-badge&logo=ruff&logoColor=white" alt="Badge">
<img src="https://img.shields.io/badge/Uv-FFC131?style=for-the-badge&logo=astral&logoColor=white" alt="Badge">
</p>

Simple python library to async use https://check-host.net/about/api

## Features

- **Fully Asynchronous**: Built on top of `httpx` for non-blocking I/O.
- **Zero Boilerplate**: No client initialization required. Just a single function call.
- **Auto-Polling**: Automatically waits for all nodes to complete the check and returns the final result.
- **Foolproof**: Strict input validation for types, ports, and check types.

## Installation

Install via pip:
```bash
pip install aiohost
```

Or using `uv`:
```bash
uv add aiohost
```

## Usage

### Basic Check
The simplest way to check a host. The function will automatically initiate the check, poll the API, and return the final result.

```python
import asyncio
from aiohost import check

async def main():
    # Check TCP port 443 on google.com using 3 random nodes
    result = await check("tcp", "google.com", port=443, max_nodes=3)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Check (Specific Nodes)
You can specify exact nodes to use for the check.

```python
import asyncio
from aiohost import check

async def main():
    result = await check(
        check_type="ping",
        host="1.1.1.1",
        max_nodes=2,
        nodes=["us1.node.check-host.net", "de1.node.check-host.net"]
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Error Handling
The library raises standard Python exceptions for invalid inputs or API errors.

```python
import asyncio
from aiohost import check

async def main():
    try:
        # This will raise a ValueError due to invalid port
        await check("tcp", "google.com", port=99999)
    except ValueError as e:
        print(f"Validation Error: {e}")
    except RuntimeError as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### `check`
Initiates a check and returns the final result dictionary.

```python
async def check(
    check_type: Literal["ping", "http", "tcp", "dns", "udp"],
    host: str,
    port: Optional[int] = None,
    max_nodes: int = 3,
    max_wait: float = 30.0,
    poll_interval: float = 1.5,
    nodes: Optional[List[str]] = None,
) -> Dict[str, Any]
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `check_type` | `str` | *Required* | Type of check: `"ping"`, `"http"`, `"tcp"`, `"dns"`, or `"udp"`. |
| `host` | `str` | *Required* | Target hostname or IP address. |
| `port` | `int` | `None` | Target port (required for `tcp`/`udp`, optional for others). Must be 1-65535. |
| `max_nodes` | `int` | `3` | Number of random nodes to use for the check. |
| `max_wait` | `float` | `30.0` | Maximum time in seconds to wait for all nodes to finish. |
| `poll_interval`| `float` | `1.5` | Time in seconds between polling the API for results. |
| `nodes` | `List[str]`| `None` | Optional list of specific node hostnames to use (overrides `max_nodes`). |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.