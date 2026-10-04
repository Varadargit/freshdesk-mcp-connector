from mcp.server.fastmcp import FastMCP

from .freshdesk_client import FreshdeskAPIError, FreshdeskClient


mcp = FastMCP("Freshdesk Connector")

_client = None


def get_client():
    """
    Create the Freshdesk client only when it is needed.
    This makes the MCP server easier to test locally.
    """

    global _client

    if _client is None:
        _client = FreshdeskClient()

    return _client


@mcp.tool()
def list_tickets(page: int = 1, per_page: int = 30) -> list:
    """
    List Freshdesk tickets.

    Args:
        page: Page number starting from 1.
        per_page: Number of tickets to return, between 1 and 100.
    """

    try:
        return get_client().list_tickets(
            page=page,
            per_page=per_page
        )

    except FreshdeskAPIError as exc:
        return {
            "error": str(exc)
        }

    except ValueError as exc:
        return {
            "error": str(exc)
        }


@mcp.tool()
def get_ticket(ticket_id: int) -> dict:
    """
    Get a single Freshdesk ticket by ID.

    Args:
        ticket_id: Freshdesk ticket ID.
    """

    try:
        return get_client().get_ticket(ticket_id)

    except FreshdeskAPIError as exc:
        return {
            "error": str(exc)
        }

    except ValueError as exc:
        return {
            "error": str(exc)
        }


@mcp.tool()
def search_tickets(query: str, page: int = 1) -> list:
    """
    Search Freshdesk tickets.

    Args:
        query: Search query for Freshdesk tickets.
        page: Page number starting from 1.
    """

    try:
        return get_client().search_tickets(
            query=query,
            page=page
        )

    except FreshdeskAPIError as exc:
        return {
            "error": str(exc)
        }

    except ValueError as exc:
        return {
            "error": str(exc)
        }


if __name__ == "__main__":
    mcp.run()