import os

from dotenv import load_dotenv


load_dotenv()


FRESHDESK_DOMAIN = os.getenv("FRESHDESK_DOMAIN")
FRESHDESK_API_KEY = os.getenv("FRESHDESK_API_KEY")


if not FRESHDESK_DOMAIN:
    raise RuntimeError("FRESHDESK_DOMAIN is not configured")

if not FRESHDESK_API_KEY:
    raise RuntimeError("FRESHDESK_API_KEY is not configured")


BASE_URL = f"https://{FRESHDESK_DOMAIN}/api/v2"