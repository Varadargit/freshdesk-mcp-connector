import httpx
import pytest

from src.freshdesk_client import FreshdeskClient, FreshdeskAPIError


def test_list_tickets(mocker):
    mock_response = httpx.Response(
        200,
        json=[
            {
                "id": 101,
                "subject": "Payment failed",
                "status": 2
            },
            {
                "id": 102,
                "subject": "Unable to login",
                "status": 2
            }
        ]
    )

    mocker.patch(
        "httpx.Client.request",
        return_value=mock_response
    )

    client = FreshdeskClient()

    try:
        tickets = client.list_tickets(page=1, per_page=5)

        assert len(tickets) == 2
        assert tickets[0]["id"] == 101
        assert tickets[0]["subject"] == "Payment failed"

    finally:
        client.close()


def test_get_ticket(mocker):
    mock_response = httpx.Response(
        200,
        json={
            "id": 101,
            "subject": "Payment failed",
            "status": 2,
            "priority": 3
        }
    )

    mocker.patch(
        "httpx.Client.request",
        return_value=mock_response
    )

    client = FreshdeskClient()

    try:
        ticket = client.get_ticket(101)

        assert ticket["id"] == 101
        assert ticket["subject"] == "Payment failed"
        assert ticket["priority"] == 3

    finally:
        client.close()


def test_invalid_ticket_id():
    client = FreshdeskClient()

    try:
        with pytest.raises(ValueError):
            client.get_ticket(0)
    finally:
        client.close()


def test_invalid_page():
    client = FreshdeskClient()

    try:
        with pytest.raises(ValueError):
            client.list_tickets(page=0)
    finally:
        client.close()


def test_invalid_per_page():
    client = FreshdeskClient()

    try:
        with pytest.raises(ValueError):
            client.list_tickets(per_page=101)
    finally:
        client.close()


def test_empty_search_query():
    client = FreshdeskClient()

    try:
        with pytest.raises(ValueError):
            client.search_tickets("")
    finally:
        client.close()


def test_rate_limit_error(mocker):
    mock_response = httpx.Response(
        429,
        headers={
            "Retry-After": "0"
        }
    )

    mocker.patch(
        "httpx.Client.request",
        return_value=mock_response
    )

    client = FreshdeskClient()

    try:
        with pytest.raises(FreshdeskAPIError):
            client.list_tickets()
    finally:
        client.close()