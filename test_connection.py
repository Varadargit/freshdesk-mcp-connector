from src.freshdesk_client import FreshdeskClient


def main():
    client = FreshdeskClient()

    try:
        tickets = client.list_tickets(page=1, per_page=5)

        print("Freshdesk connection successful!")
        print(f"Tickets returned: {len(tickets)}")

        for ticket in tickets:
            print(
                f"ID: {ticket.get('id')} | "
                f"Subject: {ticket.get('subject')} | "
                f"Status: {ticket.get('status')}"
            )

    finally:
        client.close()


if __name__ == "__main__":
    main()