"""
Cove support desk — the shared world for all seven technique demos.
--------------------------------------------------------------------
One fictional company, one messy ticket, one rule book, one set of tools.
Every technique file imports from here, so the *scenario* stays identical and
the only thing that changes between demos is the *technique*. That's the point:
technique isolated from domain.

Cove is a fictional online store with a mobile app. Any resemblance to a real
company is coincidental.

Run any demo with:  export GEMINI_API_KEY=...   then   python zero_shot.py
"""

import os
import json

from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "Set GEMINI_API_KEY or GOOGLE_API_KEY before running a demo."
    )

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-3.6-flash"

COMPANY = "Cove"

# The fixed label set for triage.
INTENTS = ["ORDER_ISSUE", "REFUND_REQUEST", "SHIPPING", "ACCOUNT", "APP_BUG", "GENERAL"]

# The running ticket — deliberately messy and multi-issue (an app bug AND a
# double charge AND a refund demand), so it stress-tests every technique.
TICKET = (
    "I tried to check out twice and the app crashed both times, but I still got "
    "charged for BOTH orders. I've been a customer for years and I just want my "
    "money back. Order numbers 4471 and 4472."
)

# The rule book (used by the chain-of-thought and ReAct demos).
REFUND_POLICY = """Cove refund rules:
- An order that was charged but never shipped is refunded in full (item + shipping).
- A shipped order that is returned: refund the ITEM price minus a 10% restocking
  fee; shipping is non-refundable.
- For a confirmed app fault affecting the customer, add a one-time $10 goodwill
  credit (once, not per order)."""


def ask(prompt: str, system: str | None = None,
        temperature: float = 0.0, max_tokens: int = 1024) -> str:
    """One call to the model. Every demo routes through this so the shape of an
    API call is identical everywhere — only the prompt (and a few knobs) change."""
    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    if system:
        config.system_instruction = system

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config,
    )
    return response.text


# ---- Tool stubs (used only by the ReAct demo) --------------------------------
# In real life these hit your database / order service. Here they're canned so
# the demo is deterministic. The numbers line up with the self-consistency demo.
_ORDERS = {
    "4471": {"status": "charged_not_shipped", "item": 130, "shipping": 18},
    "4472": {"status": "charged_and_shipped", "item": 130, "shipping": 18},
}
_CUSTOMERS = {
    "sarah@example.com": {"name": "Sarah", "customer_since": 2019,
                          "orders": ["4471", "4472"]},
}


def get_customer(email: str) -> str:
    c = _CUSTOMERS.get(email)
    return json.dumps(c) if c else f"No customer found for {email}"


def get_order(order_id: str) -> str:
    o = _ORDERS.get(str(order_id))
    return json.dumps(o) if o else f"No order found: {order_id}"


def get_refund_policy() -> str:
    return REFUND_POLICY
