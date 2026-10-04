import time

import httpx

from .config import BASE_URL, FRESHDESK_API_KEY
from .models import sanitize_ticket


class FreshdeskAPIError(Exception):
    """Raised when a Freshdesk API request fails."""


class FreshdeskClient:
    def __init__(self):
        self.client = httpx.Client(
            auth=(FRESHDESK_API_KEY, "X"),
            headers={
                "Accept": "application/json"
            },
            timeout=30.0
        )

    def _request(self, method, endpoint, **kwargs):
        url = f"{BASE_URL}{endpoint}"

        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.client.request(
                    method,
                    url,
                    **kwargs
                )

                # Handle rate limiting
                if response.status_code == 429:
                    if attempt == max_retries - 1:
                        raise FreshdeskAPIError(
                            "Freshdesk rate limit exceeded."
                        )

                    retry_after = response.headers.get("Retry-After")

                    if retry_after:
                        delay = int(retry_after)
                    else:
                        delay = 2 ** attempt

                    time.sleep(delay)
                    continue

                # Handle temporary Freshdesk server errors
                if response.status_code >= 500:
                    if attempt == max_retries - 1:
                        raise FreshdeskAPIError(
                            f"Freshdesk server error: "
                            f"{response.status_code}"
                        )

                    time.sleep(2 ** attempt)
                    continue

                # Handle other API errors
                if response.status_code >= 400:
                    raise FreshdeskAPIError(
                        f"Freshdesk API error "
                        f"{response.status_code}: {response.text}"
                    )

                return response.json()

            except httpx.RequestError as exc:
                if attempt == max_retries - 1:
                    raise FreshdeskAPIError(
                        f"Network error while contacting Freshdesk: {exc}"
                    ) from exc

                time.sleep(2 ** attempt)

        raise FreshdeskAPIError("Freshdesk request failed.")

    def list_tickets(self, page=1, per_page=30):
        """
        Return a paginated list of Freshdesk tickets.
        """

        if page < 1:
            raise ValueError(
                "page must be greater than or equal to 1"
            )

        if not 1 <= per_page <= 100:
            raise ValueError(
                "per_page must be between 1 and 100"
            )

        tickets = self._request(
            "GET",
            "/tickets",
            params={
                "page": page,
                "per_page": per_page
            }
        )

        return [
            sanitize_ticket(ticket)
            for ticket in tickets
        ]

    def get_ticket(self, ticket_id):
        """
        Return a single Freshdesk ticket by ID.
        """

        if ticket_id <= 0:
            raise ValueError(
                "ticket_id must be a positive integer"
            )

        ticket = self._request(
            "GET",
            f"/tickets/{ticket_id}"
        )

        return sanitize_ticket(ticket)

    def search_tickets(self, query, page=1):
        """
        Search Freshdesk tickets.
        """

        if not query or not query.strip():
            raise ValueError(
                "query cannot be empty"
            )

        if page < 1:
            raise ValueError(
                "page must be greater than or equal to 1"
            )

        response = self._request(
            "GET",
            "/search/tickets",
            params={
                "query": query,
                "page": page
            }
        )

        tickets = response.get("results", [])

        return [
            sanitize_ticket(ticket)
            for ticket in tickets
        ]

    def close(self):
        """
        Close the HTTP client.
        """

        self.client.close()