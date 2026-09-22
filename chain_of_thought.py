"""
CHAIN-OF-THOUGHT — reason through the refund rules before deciding.
Sub-task: decide how Cove should handle this ticket under the refund policy.
"""
from cove_desk import ask, TICKET, REFUND_POLICY

prompt = f"""{REFUND_POLICY}

Ticket: "{TICKET}"
Known facts: Order 4471 was charged but never shipped. Order 4472 was charged and shipped.

Work through it step by step:
1. Which rule applies to which order?
2. Does the app-fault goodwill credit apply?
Then, on the LAST line only, output exactly:
VERDICT: <APPROVE_FULL | APPROVE_PARTIAL | ESCALATE>"""

print("CHAIN-OF-THOUGHT refund decision\n")
print(ask(prompt))

print(
    "\nNotice: the working is visible and auditable — you can see WHY it reached "
    "the verdict, which is what you want when money is on the line. And the "
    "decision is pinned to the last line in a fixed vocabulary, so your code can "
    "parse it. Don't reach for this on plain extraction or classification — "
    "you'd pay for reasoning tokens you don't need."
)
