# Simple Toolsets Wrapper

A simple wrapper script to wrap any MCP server using the [Gradio Toolsets](https://github.com/gradio-app/toolsets) library.

## Features

- Wrap any MCP server URL with a single command
- Support for deferred loading (minimal context window usage)
- Configurable port and toolset name
- Semantic search for discovering tools when using deferred mode

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python wrap_server.py <server_url> [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `server_url` | The MCP server URL to wrap (required) |

### Options

| Option | Description |
|--------|-------------|
| `--deferred` | Use deferred loading (minimal context) |
| `--port PORT` | Port to run on (default: 7860) |
| `--name NAME` | Name for the toolset (default: "Wrapped MCP Server") |
| `--notes NOTES` | Description notes for deferred discovery |

### Examples

```bash
# Wrap a local MCP server
python wrap_server.py http://localhost:8000/mcp

# Wrap with deferred loading (recommended for servers with many tools)
python wrap_server.py http://localhost:8000/mcp --deferred

# Wrap a HuggingFace Space
python wrap_server.py https://some-space.hf.space/gradio_api/mcp/ --deferred

# Custom port and name
python wrap_server.py http://localhost:8000/mcp --port 7861 --name "MyServer"
```

## Modes

### Direct Mode (default)
All tools from the wrapped server are loaded directly into context. Best for servers with a small number of tools.

### Deferred Mode (`--deferred`)
Tools are not loaded into context. Instead, two special tools are exposed:
- `search_deferred_tools` - Semantic search to find relevant tools
- `call_deferred_tool` - Execute a discovered tool

This dramatically reduces context window usage while providing access to all functionality.

## Output

The wrapped MCP endpoint will be available at:
```
http://localhost:<port>/gradio_api/mcp
```

## License

GPL-3.0
