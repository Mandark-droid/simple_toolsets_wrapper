"""
MCP Server Wrapper - Wrap any MCP server with Gradio Toolsets

This script wraps a single MCP server URL, optionally with deferred loading,
making it accessible through a Gradio Toolsets endpoint.

Usage:
    python wrap_server.py <server_url> [options]

    Arguments:
        server_url      The MCP server URL to wrap (required)

    Options:
        --deferred      Use deferred loading (minimal context)
        --port PORT     Port to run on (default: 7860)
        --name NAME     Name for the toolset (default: "Wrapped MCP Server")
        --notes NOTES   Description notes for deferred discovery

Examples:
    # Wrap TraceVerde server
    python wrap_server.py http://localhost:8000/mcp

    # Wrap with deferred loading
    python wrap_server.py http://localhost:8000/mcp --deferred

    # Wrap HuggingFace space
    python wrap_server.py https://some-space.hf.space/gradio_api/mcp/ --deferred

    # Custom port and name
    python wrap_server.py http://localhost:8000/mcp --port 7861 --name "TraceVerde"

The wrapped MCP endpoint will be available at:
    http://localhost:<port>/gradio_api/mcp
"""

import argparse
import os
import sys

from toolsets import Server, Toolset


def create_wrapped_toolset(
    server_url: str,
    name: str = "Wrapped MCP Server",
    deferred: bool = False,
    notes: str = ""
):
    """
    Create a toolset wrapping a single MCP server.

    Args:
        server_url: The MCP server URL to wrap
        name: Name for the toolset
        deferred: Whether to use deferred loading
        notes: Description notes for semantic search (used with deferred)

    Returns:
        Configured Toolset instance
    """
    toolset = Toolset(
        name,
        tool_description_format="[{toolset_name}] {tool_description}"
    )

    mode_str = "(deferred)" if deferred else "(direct)"
    print(f"\nWrapping MCP server {mode_str}: {server_url}")

    try:
        toolset.add(
            Server(server_url),
            defer_loading=deferred,
            notes=notes if notes else f"Tools from {server_url}"
        )
        print(f"  + Successfully connected to server")
    except Exception as e:
        print(f"  - Failed to connect: {type(e).__name__}: {e}")
        sys.exit(1)

    return toolset


def main():
    parser = argparse.ArgumentParser(
        description="Wrap an MCP server with Gradio Toolsets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python wrap_server.py http://localhost:8000/mcp
  python wrap_server.py http://localhost:8000/mcp --deferred
  python wrap_server.py http://localhost:8000/mcp --port 7861 --name "MyServer"
        """
    )

    parser.add_argument(
        "server_url",
        help="The MCP server URL to wrap"
    )
    parser.add_argument(
        "--deferred",
        action="store_true",
        help="Use deferred loading (exposes search_deferred_tools and call_deferred_tool)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to run on (default: 7860)"
    )
    parser.add_argument(
        "--name",
        default="Wrapped MCP Server",
        help="Name for the toolset (default: 'Wrapped MCP Server')"
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Description notes for deferred discovery"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("MCP Server Wrapper")
    print("=" * 60)

    if args.deferred:
        print("""
Mode: DEFERRED
==============
- Tools are not loaded directly in context
- 2 special tools exposed:
  * search_deferred_tools - Find tools by description
  * call_deferred_tool - Execute a discovered tool
""")
    else:
        print("""
Mode: DIRECT
============
- All tools loaded directly in context
- Immediate access to all server tools
""")

    toolset = create_wrapped_toolset(
        server_url=args.server_url,
        name=args.name,
        deferred=args.deferred,
        notes=args.notes
    )

    print()
    print("=" * 60)
    print("Starting wrapped server...")

    # Set port via Gradio environment variable
    os.environ["GRADIO_SERVER_PORT"] = str(args.port)
    print(f"MCP Endpoint: http://localhost:{args.port}/gradio_api/mcp")
    print("=" * 60)

    toolset.launch(mcp_server=True)


if __name__ == "__main__":
    main()
