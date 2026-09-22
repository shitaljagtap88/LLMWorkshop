"""
ZERO-SHOT — classify the ticket's intent with no examples, just an instruction.
Sub-task in the Cove spine: first-touch triage of an incoming ticket.
"""
from cove_desk import ask, TICKET, INTENTS

prompt = f"""Classify this customer support ticket into exactly ONE intent from:
{", ".join(INTENTS)}
Reply with only the label, nothing else.

Ticket: "{TICKET}"
"""

print("ZERO-SHOT classification\n")
print("Ticket:", TICKET, "\n")
print("Model's label:", ask(prompt).strip())

print(
    "\nNotice: no examples, just an instruction. Fast and perfectly fine for "
    "clear-cut tickets. But this ticket carries TWO issues — an app crash and a "
    "refund demand — so watch which one it picks, and whether it ever strays "
    "outside the six labels. That wobble is exactly what few-shot fixes next."
)
