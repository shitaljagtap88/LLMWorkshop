# LLMWorkshop

Prompting technique demos on one shared Cove support-desk scenario.

Each script isolates a technique; `cove_desk.py` holds the ticket, policy, and model client.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export GEMINI_API_KEY=your-key   # Windows: set GEMINI_API_KEY=your-key
```

`GOOGLE_API_KEY` is accepted as a fallback.

## Demos

| Script | Technique |
| --- | --- |
| `main.py` | Smoke test (`Hello World`) |
| `zero_shot.py` | Classify with instruction only |
| `few_shot.py` | Classify with labeled examples |
| `role_prompting.py` | Persona in the system message |
| `directional_stimulus.py` | Hint keywords in the user prompt |
| `chain_of_thought.py` | Step-by-step refund verdict |
| `self_consistency.py` | Sample CoT several times and vote |
| `react.py` | Reason + Act tool loop |

```bash
python zero_shot.py
```
