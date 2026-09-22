"""
SELF-CONSISTENCY — sample the refund CALCULATION several times, take the vote.
Sub-task: compute the exact refund total, where a single slip is expensive.

NOT a prompt — a loop around the model:
  1. Ask the same chain-of-thought problem N times at temperature > 0
  2. Parse the final number from each
  3. Take the majority vote
"""
import re
from collections import Counter

from cove_desk import ask

N_SAMPLES = 7        # odd, so a two-way vote can't tie
TEMPERATURE = 0.8    # > 0 is REQUIRED, or every sample is identical

PROBLEM = """Compute the TOTAL refund Cove owes this customer.
- Order 4471: charged $148 (item $130 + shipping $18), never shipped.
- Order 4472: charged $148 (item $130 + shipping $18), shipped, now being returned.

Rules:
- An order that never shipped: refund in full (item + shipping).
- A returned shipped order: refund the ITEM price minus a 10% restocking fee;
  shipping is non-refundable.
- Confirmed app fault: add a one-time $10 goodwill credit (once, not per order).

Think step by step. On the LAST line, output exactly:
ANSWER: <integer dollars, digits only, no $ sign or commas>"""

ANSWER_RE = re.compile(r"ANSWER:\s*([0-9]+)", re.IGNORECASE)


def one_sample():
    text = ask(PROBLEM, temperature=TEMPERATURE)
    m = ANSWER_RE.search(text)
    return int(m.group(1)) if m else None


print(f"SELF-CONSISTENCY — {N_SAMPLES} samples at temperature {TEMPERATURE}\n")

answers = []
for i in range(N_SAMPLES):
    a = one_sample()
    answers.append(a)
    print(f"  sample {i + 1}: {a}")

valid = [a for a in answers if a is not None]
if not valid:
    print("\nNo parseable answers — tighten the ANSWER: instruction.")
else:
    votes = Counter(valid)
    winner, count = votes.most_common(1)[0]
    print("\nVote tally:", dict(votes))
    print(f"Self-consistency answer: ${winner}  ({count}/{len(valid)} agreed)")
    print("Correct answer:          $275   (148 + 117 + 10)")
    print(
        "\nNotice: some samples slip — they forget the $10 credit ($265), or "
        "refund 4472 in full ($296+), or take 10% off the wrong number. The vote "
        "outweighs the slips. If all 7 agree, the problem's too easy for this "
        "model — raise temperature or add a step until they diverge. The point "
        "only lands when the samples disagree and the majority still wins."
    )
