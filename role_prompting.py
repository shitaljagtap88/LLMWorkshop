"""
ROLE — the same drafting task, with and without a persona in the system message.
Sub-task: write the customer-facing reply in Cove's voice.
"""
from cove_desk import ask, TICKET

task = f'Write a short reply to this customer.\n\nTicket: "{TICKET}"'

# No role: just the task.
plain = ask(task, temperature=0.7)

# Same task, but a persona + standards live in the SYSTEM message.
ROLE = (
    "You are a senior support agent for Cove, an online store. You are warm but "
    "concise, you take clear responsibility when something breaks, and you NEVER "
    "promise a specific refund amount before it has been verified — you say it is "
    "being processed. Keep it to two to four sentences."
)
with_role = ask(task, system=ROLE, temperature=0.7)

print("WITHOUT a role:\n")
print(plain)
print("\n" + "-" * 60 + "\n")
print("WITH the senior-agent role:\n")
print(with_role)

print(
    "\nNotice: same task, same model, same temperature. The only change lives in "
    "the SYSTEM message — and it shifts voice, ownership, and length, and it adds "
    "a hard guardrail (no unverified refund promises) that never appeared in the "
    "user's message. Durable rules go in system; the changing task goes in user."
)
