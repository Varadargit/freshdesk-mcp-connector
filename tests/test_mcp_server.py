from src import mcp_server


class FakeFreshdeskClient:
    """Fake Freshdesk client used for local MCP testing."""

    def list_tickets(self, page=1, per_page=30):
        return [
            {
                "id": 101,
                "subject": "Payment failed",
                "status": 2,
                "priority": 3
            },
            {
                "id": 102,
                "subject": "Unable to login",
                "status": 2,
                "priority": 2
            }
        ]

    def get_ticket(self, ticket_id):
        return {
            "id": ticket_id,
            "subject": "Payment failed",
            "status": 2,
            "priority": 3
        }

    def search_tickets(self, query, page=1):
        return [
            {
                "id": 101,
                "subject": "Payment failed",
                "status": 2,
                "priority": 3
            }
        ]


def setup_fake_client():
    """
    Replace the real Freshdesk client with a fake client.
    This prevents any real API calls during testing.
    """

    mcp_server._client = FakeFreshdeskClient()


def test_list_tickets_tool():
    setup_fake_client()

    result = mcp_server.list_tickets(
        page=1,
        per_page=10
    )

    assert len(result) == 2
    assert result[0]["id"] == 101
    assert result[0]["subject"] == "Payment failed"


def test_get_ticket_tool():
    setup_fake_client()

    result = mcp_server.get_ticket(101)

    assert result["id"] == 101
    assert result["subject"] == "Payment failed"


def test_search_tickets_tool():
    setup_fake_client()

    result = mcp_server.search_tickets(
        query="payment failed"
    )

    assert len(result) == 1
    assert result[0]["id"] == 101


def test_invalid_ticket_id():
    setup_fake_client()

    result = mcp_server.get_ticket(0)

    assert "error" in result


def test_invalid_search_query():
    setup_fake_client()

    result = mcp_server.search_tickets("")

    assert "error" in result