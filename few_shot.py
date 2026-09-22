"""
FEW-SHOT — the same classification, now with a handful of labeled examples.
Sub-task: lock the output format and settle the tricky multi-issue tickets.
"""
from cove_desk import ask, TICKET, INTENTS

EXAMPLES = """Ticket: "Where's my parcel? It's five days late." -> SHIPPING
Ticket: "The app won't load past the login screen." -> APP_BUG
Ticket: "You charged me twice by mistake, please reverse one." -> REFUND_REQUEST
Ticket: "How do I change the email on my account?" -> ACCOUNT"""

prompt = f"""Classify each ticket into exactly ONE intent from:
{", ".join(INTENTS)}
When a ticket raises several issues, pick the PRIMARY one the customer most wants resolved.

{EXAMPLES}
Ticket: "{TICKET}" ->"""

print("FEW-SHOT classification\n")
print("Model's label:", ask(prompt).strip())

print(
    "\nNotice: two things the examples did that a paragraph of description "
    "couldn't. They fixed the OUTPUT SHAPE — just a bare label — and they taught "
    "the 'pick the primary issue' rule by DEMONSTRATION. So the double-issue "
    "ticket now lands consistently, where zero-shot could waver run to run. "
    "Rule of thumb: when format drifts, show an example instead of describing it."
)
