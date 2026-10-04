def sanitize_ticket(ticket):
    """
    Return only the fields that the AI agent needs.
    """

    return {
        "id": ticket.get("id"),
        "subject": ticket.get("subject"),
        "status": ticket.get("status"),
        "priority": ticket.get("priority"),
        "type": ticket.get("type"),
        "created_at": ticket.get("created_at"),
        "updated_at": ticket.get("updated_at"),
    }