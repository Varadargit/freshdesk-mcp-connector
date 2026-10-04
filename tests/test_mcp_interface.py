import pytest

from src import mcp_server


@pytest.mark.anyio
async def test_mcp_tools_are_registered():
    """
    Verify that the MCP server exposes the expected tools.
    """

    tools = await mcp_server.mcp.list_tools()

    tool_names = {
        tool.name
        for tool in tools
    }

    assert "list_tickets" in tool_names
    assert "get_ticket" in tool_names
    assert "search_tickets" in tool_names