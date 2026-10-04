# Freshdesk MCP Connector — System Architecture

## 1. Overview

This project implements a read-only connector between an AI agent and Freshdesk.

The connector exposes selected Freshdesk operations as MCP tools so that an AI agent can retrieve and search support-ticket information without directly handling Freshdesk API details.

The system is designed around three main principles:

- Simple integration through MCP
- Read-only access to reduce risk
- Clear separation between the AI agent, connector logic, and merchant API

### Current Scope

The connector supports:

- Listing Freshdesk tickets
- Retrieving a specific ticket
- Searching tickets
- Freshdesk API authentication
- Input validation
- Rate-limit handling
- Retry handling for temporary failures
- Response sanitization
- Automated local tests

The connector does **not** support:

- Creating tickets
- Updating tickets
- Deleting tickets
- Sending replies
- Assigning tickets
- Changing ticket status
- Modifying merchant data

The current implementation is intentionally read-only.

---

# 2. Problem Statement

A merchant support team may store a large amount of operational information inside Freshdesk.

An AI agent can be useful for questions such as:

- "Show me recent support tickets."
- "Find tickets related to payment failures."
- "Get the details of ticket 101."
- "What tickets are related to login problems?"

However, the AI agent should not need to understand Freshdesk's REST API directly.

The connector provides a controlled interface between the AI agent and Freshdesk.

Instead of exposing the entire Freshdesk API, the connector exposes a small set of well-defined tools that an agent can safely call.

---

# 3. High-Level System Architecture

```text
                         AI Agent / Agent Studio
                                  |
                                  |
                            MCP Protocol
                                  |
                                  v
                    +---------------------------+
                    |     Freshdesk MCP Server  |
                    |                           |
                    |  list_tickets             |
                    |  get_ticket               |
                    |  search_tickets           |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    |    Freshdesk Client       |
                    |                           |
                    |  Authentication           |
                    |  Validation               |
                    |  Retry handling           |
                    |  Rate-limit handling      |
                    |  Error handling           |
                    |  Response sanitization    |
                    +-------------+-------------+
                                  |
                         HTTPS REST API
                                  |
                                  v
                    +---------------------------+
                    |       Freshdesk           |
                    |       REST API            |
                    +---------------------------+

End-to-End Request Flow
User asks a question
        |
        v
AI Agent determines that Freshdesk data is required
        |
        v
Agent selects an MCP tool
        |
        v
MCP Server receives the tool request
        |
        v
Input validation
        |
        v
Freshdesk Client
        |
        v
Authenticated HTTPS request
        |
        v
Freshdesk REST API
        |
        v
Freshdesk response
        |
        v
Response sanitization
        |
        v
MCP Server returns structured data
        |
        v
AI Agent uses the result to answer the user