"""
DIRECTIONAL STIMULUS — steer the reply with hint keywords, without scripting it.
Sub-task: make sure the customer reply hits the beats that matter.
"""
from cove_desk import ask, TICKET

plain_prompt = f'Draft a reply to this customer.\n\nTicket: "{TICKET}"'

stimulus_prompt = plain_prompt + (
    "\n\nHints to weave in: apologize for the app crash; confirm the duplicate "
    "charge is being refunded; give a 5-7 business day timeline; mention the $10 "
    "goodwill credit; invite her to reply if anything is off."
)

print("PLAIN ask:\n")
print(ask(plain_prompt, temperature=0.7))
print("\n" + "-" * 60 + "\n")
print("WITH directional stimulus (hint keywords):\n")
print(ask(stimulus_prompt, temperature=0.7))

print(
    "\nNotice: the hints don't dictate the wording — the model still writes the "
    "sentences. They steer which POINTS the reply covers, so the beats that "
    "matter show up every time. Lighter than few-shot (no full examples), "
    "stronger than a bare ask. Reach for it when you know the salient points."
)
