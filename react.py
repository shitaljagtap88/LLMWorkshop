"""
ReAct — Reason + Act. The model uses tools instead of guessing.
Sub-task: verify the customer's orders before promising anything.

The model NEVER runs the tools. It names an Action; our Python runs it and feeds
back the Observation. That separation is the lesson: the model decides, code acts.
"""
import json
import re

from cove_desk import client, MODEL, get_customer, get_order, get_refund_policy

TOOLS = {
    "get_customer": get_customer,
    "get_order": get_order,
    "get_refund_policy": get_refund_policy,
}

SYSTEM = """You are a Cove support agent that answers using tools.
Respond in EXACTLY this format, one step at a time:

Thought: <your reasoning>
Action: <one of: get_customer, get_order, get_refund_policy>
Action Input: <a JSON object of arguments>

After you see an Observation, continue with the next Thought. When you have
enough information, respond instead with:

Thought: <reasoning>
Final Answer: <what you will tell the customer>

Tool signatures:
- get_customer(email)
- get_order(order_id)      # order_id as a string, e.g. {"order_id": "4471"}
- get_refund_policy()      # no arguments — pass {}"""

TASK = ("Customer sarah@example.com says both her checkout orders failed but she "
        "was charged twice. Verify what actually happened and tell her what Cove "
        "will refund.")

ACTION_RE = re.compile(r"Action:\s*(\w+)\s*Action Input:\s*(\{.*?\})", re.DOTALL)

transcript = f"Question: {TASK}\n"
print("ReAct loop\n")

for _ in range(8):  # step cap
    resp = client.models.generate_content(
        model=MODEL,
        contents=transcript,
        config={
            "system_instruction": SYSTEM,
            "max_output_tokens": 700,
            "stop_sequences": ["Observation:"],
        },
    )
    chunk = resp.text.strip()
    print(chunk, "\n")
    transcript += chunk + "\n"

    if "Final Answer:" in chunk:
        break

    m = ACTION_RE.search(chunk)
    if not m:
        print("(no valid Action parsed — stopping)")
        break

    name, args = m.group(1), json.loads(m.group(2))
    observation = TOOLS[name](**args)
    print(f"Observation: {observation}\n{'-' * 60}")
    transcript += f"Observation: {observation}\n"

print(
    "\nNotice: the model looked up the customer, then each order, discovered that "
    "4472 actually shipped (not both failed, as she believed), read the policy, "
    "and only THEN answered — grounded in real data, not a guess. The "
    'stop_sequences=["Observation:"] is what forces it to wait for OUR result '
    "instead of inventing one."
)
