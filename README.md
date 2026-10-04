# Freshdesk MCP Connector for AI Agents

A read-only MCP connector that enables an AI agent to securely retrieve and search Freshdesk support-ticket data through structured tools.

This project was built as a solution for the **Razorpay Forward-Deployed Engineer — Agent Studio** assignment.

---

## 1. What This Project Does

The connector creates a controlled interface between an AI agent and Freshdesk.

Instead of the agent directly interacting with the Freshdesk REST API, it uses MCP tools:

```text
AI Agent / Agent Studio
          |
          | MCP
          v
    MCP Server
          |
          v
  Freshdesk Client
          |
          | HTTPS REST API
          v
      Freshdesk
```

The current connector provides three read-only capabilities:

* List tickets
* Get a ticket by ID
* Search tickets

The connector also handles authentication, input validation, API errors, rate limits, retries, and response sanitization.

---

## 2. Why MCP?

The AI agent should not need to know how Freshdesk's REST API works.

MCP provides a structured tool interface that allows the agent to discover and invoke capabilities such as:

```text
list_tickets
get_ticket
search_tickets
```

This separates the agent-facing interface from the underlying Freshdesk API implementation.

---

## 3. Available Tools

### `list_tickets`

Returns a paginated list of Freshdesk tickets.

```text
list_tickets(
    page=1,
    per_page=30
)
```

Parameters:

| Parameter  | Type    | Description                                    |
| ---------- | ------- | ---------------------------------------------- |
| `page`     | integer | Page number starting from 1                    |
| `per_page` | integer | Number of tickets to return, between 1 and 100 |

---

### `get_ticket`

Retrieves a single ticket by ID.

```text
get_ticket(
    ticket_id=101
)
```

Parameters:

| Parameter   | Type    | Description         |
| ----------- | ------- | ------------------- |
| `ticket_id` | integer | Freshdesk ticket ID |

---

### `search_tickets`

Searches Freshdesk tickets.

```text
search_tickets(
    query="payment failure",
    page=1
)
```

Parameters:

| Parameter | Type    | Description                   |
| --------- | ------- | ----------------------------- |
| `query`   | string  | Freshdesk ticket search query |
| `page`    | integer | Page number starting from 1   |

---

## 4. Read-Only Scope

The connector intentionally exposes only read operations.

Supported:

```text
list_tickets
get_ticket
search_tickets
```

Not supported:

```text
create_ticket
update_ticket
delete_ticket
reply_to_ticket
assign_ticket
change_ticket_status
```

This keeps the integration low-risk and prevents the AI agent from modifying merchant data.

---

## 5. Project Structure

```text
razorpay-freshdesk-connector/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── freshdesk_client.py
│   ├── models.py
│   └── mcp_server.py
│
├── tests/
│   ├── test_freshdesk_client.py
│   ├── test_mcp_server.py
│   └── test_mcp_interface.py
│
├── docs/
│   └── architecture.md
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── test_connection.py
└── README.md
```

### Source files

**`src/mcp_server.py`**

Defines and exposes the MCP tools.

**`src/freshdesk_client.py`**

Handles Freshdesk API communication, authentication, validation, retries, rate limits, and errors.

**`src/models.py`**

Sanitizes Freshdesk responses before returning them to the AI agent.

**`src/config.py`**

Loads Freshdesk configuration from environment variables.

---

## 6. Requirements

* Python 3.10+
* Freshdesk account/API credentials for live API testing
* Internet access for live Freshdesk API requests

Real Freshdesk credentials are **not required for the automated test suite**, because API calls are mocked.

---

## 7. Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd razorpay-freshdesk-connector
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 8. Configuration

Create a `.env` file in the project root.

```env
FRESHDESK_DOMAIN=your-domain.freshdesk.com
FRESHDESK_API_KEY=your_api_key_here
```

Do not include:

```text
https://
```

in `FRESHDESK_DOMAIN`.

Example:

```env
FRESHDESK_DOMAIN=mycompany.freshdesk.com
FRESHDESK_API_KEY=your_api_key_here
```

The API key must not be committed to Git.

The repository includes `.env.example` as a configuration template.

---

## 9. Running the Tests

The project can be tested without a real Freshdesk account.

Run:

```bash
python -m pytest
```

The test suite verifies:

* Freshdesk client behavior
* Input validation
* API error handling
* Rate-limit handling
* MCP tool behavior
* MCP tool registration

Current local result:

```text
13 passed
```

---

## 10. Testing Without Freshdesk

The automated tests use mocked HTTP responses and a fake Freshdesk client.

This means:

```text
pytest
   |
   v
MCP Server
   |
   v
Fake / Mock Freshdesk layer
   |
   v
Assertions
```

No real merchant data is accessed during the test suite.

This makes local development safe and reproducible.

---

## 11. Testing a Real Freshdesk Connection

Once valid Freshdesk credentials are available, the connection can be tested using:

```bash
python test_connection.py
```

The script calls the Freshdesk API and retrieves a small page of tickets.

Expected output is similar to:

```text
Freshdesk connection successful!
Tickets returned: 5
ID: 101 | Subject: Payment failed | Status: 2
...
```

Do not run this script without valid Freshdesk credentials.

---

## 12. Error and Reliability Handling

The connector handles several failure scenarios.

### Invalid input

Examples:

```text
page = 0
ticket_id = 0
per_page = 101
query = ""
```

These are rejected before making an API request.

### HTTP errors

Freshdesk API errors are converted into controlled application errors.

### Rate limiting

HTTP `429` responses are handled using:

1. `Retry-After` when provided
2. Exponential backoff otherwise
3. A limited number of retry attempts

### Temporary server failures

HTTP `5xx` responses are retried with exponential backoff.

### Network failures

Temporary network errors are retried before returning a controlled failure.

The connector never retries indefinitely.

---

## 13. Response Sanitization

Freshdesk responses may contain more information than the AI agent needs.

The connector returns a limited set of ticket fields.

Example:

```json
{
  "id": 101,
  "subject": "Payment failed",
  "status": 2,
  "priority": 3,
  "type": "Question",
  "created_at": "2026-10-01T10:30:00Z",
  "updated_at": "2026-10-01T11:00:00Z"
}
```

This keeps the tool response predictable and avoids unnecessarily exposing the complete upstream response.

---

## 14. Security

The project follows several basic security principles:

* API credentials are loaded from environment variables.
* Credentials are not hardcoded.
* `.env` is excluded from Git.
* `.env.example` contains placeholders only.
* The MCP interface is read-only.
* API responses are sanitized before being returned to the agent.
* Automated tests do not access real merchant data.

The AI agent does not need direct access to the Freshdesk API key.

---

## 15. Agent Interaction Example

A user could ask an AI agent:

```text
"Find tickets related to payment failures."
```

The agent can select:

```text
search_tickets(
    query="payment failure",
    page=1
)
```

The connector then:

```text
1. Validates the request
2. Authenticates with Freshdesk
3. Calls the Freshdesk REST API
4. Handles retries/rate limits if required
5. Sanitizes the response
6. Returns structured data to the agent
```

The agent can then use that result to answer the user's question.

---

## 16. Architecture

The detailed system architecture is documented separately in:

```text
docs/architecture.md
```

The main request path is:

```text
AI Agent / Agent Studio
          |
          v
      MCP Server
          |
          v
   Freshdesk Client
          |
          v
   Freshdesk REST API
```

---

## 17. Current Implementation Status

### Implemented

* [x] Freshdesk API client
* [x] API-key authentication
* [x] MCP server
* [x] `list_tickets`
* [x] `get_ticket`
* [x] `search_tickets`
* [x] Input validation
* [x] Rate-limit handling
* [x] Retry logic
* [x] Error handling
* [x] Response sanitization
* [x] Automated tests
* [x] MCP tool registration tests
* [x] Architecture documentation

### Not currently implemented

* [ ] Write operations
* [ ] Production deployment
* [ ] Persistent caching
* [ ] Production secrets management
* [ ] Live Agent Studio deployment/configuration

The MCP connector and its local tests are implemented. A production Agent Studio integration would require deploying the MCP server and configuring the deployed endpoint in the target environment.

---

## 18. Limitations

The current implementation intentionally has a small scope.

1. It supports only Freshdesk.
2. It currently exposes ticket read operations only.
3. It does not modify merchant data.
4. Only selected ticket fields are returned.
5. It does not currently implement persistent caching.
6. A production deployment is not included in the local project.

These limitations keep the initial connector focused while leaving a clear path for future extensions.

---

## 19. Future Improvements

Potential extensions include:

```text
list_contacts
get_contact
list_ticket_conversations
list_agents
```

Additional production capabilities could include:

* Secure secrets management
* Structured logging
* Metrics and observability
* Response caching
* Containerized deployment
* Authentication for the MCP endpoint
* Controlled write operations with additional authorization

---

## 20. Assignment Scope

This project was built for the **Razorpay Forward-Deployed Engineer — Agent Studio** assignment.

The selected assignment is the private merchant-tool connector.

Chosen merchant system:

```text
Freshdesk
```

The connector demonstrates how an AI agent can access merchant support data through a controlled MCP interface while keeping API authentication and integration logic inside the connector.

No real customer data is included in the repository.

---

## 21. Summary

The project provides a lightweight bridge between an AI agent and Freshdesk:

```text
User
  |
  v
AI Agent
  |
  v
MCP Tools
  |
  v
Freshdesk Client
  |
  v
Freshdesk API
```

The connector provides a small, controlled, read-only interface while handling the underlying API complexity.

The design emphasizes:

* Clear tool boundaries
* Secure credential handling
* Input validation
* API resilience
* Response minimization
* Testability
* Extensibility

For detailed system design and request flow, see:

```text
docs/architecture.md
```
