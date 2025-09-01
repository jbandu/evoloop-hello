# triage.py
from __future__ import annotations
import os, sys, json
from dotenv import load_dotenv
from openai import OpenAI

# Load env
load_dotenv()
api_key = os.getenv("XAI_API_KEY") or os.getenv("GROK_API_KEY")
if not api_key:
    print("Missing XAI_API_KEY or GROK_API_KEY in your environment/.env", file=sys.stderr)
    sys.exit(1)

# xAI is OpenAI-compatible; just point the client at xAI's base URL
client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

# Default feature; override by setting FEATURE_JSON env var (optional)
feature = json.loads(os.getenv("FEATURE_JSON") or json.dumps({
    "title": "Hello World Counter",
    "description": "Web app with counter and dark mode toggle",
    "votes": 10
}))

def chat_json(model: str, system_msg: str, user_msg: str) -> dict:
    """Call chat.completions and guarantee a JSON object back."""
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_msg},
                  {"role": "user", "content": user_msg}],
        temperature=0,
        response_format={"type": "json_object"},   # force valid JSON
    )
    text = resp.choices[0].message.content
    try:
        return json.loads(text)
    except Exception:
        # Best-effort JSON extraction if the model wrapped it with text
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start:end+1])
        raise RuntimeError(f"Model did not return JSON:\n{text}")

def triage_feature(f: dict) -> dict:
    system = (
        "You are an AI triage agent. Output ONLY a JSON object with keys: "
        "summary, priority, status. priority is 0-100 based on votes "
        "(e.g., 10 votes → 80). status must be 'triaged'."
    )
    user = f"Feature: {f['title']}\nDescription: {f['description']}\nVotes: {f['votes']}"
    return chat_json("grok-3", system, user)

def generate_spec(t: dict) -> dict:
    system = (
        "You are an AI spec agent. Output ONLY JSON with keys: "
        "problem, scope, acceptance_criteria (string[]), tasks (string[]), test_plan (string[]). "
        "Be concise and implementable."
    )
    user = "Triaged feature:\n" + json.dumps(t, ensure_ascii=False)
    return chat_json("grok-3", system, user)

if __name__ == "__main__":
    triage = triage_feature(feature)
    print("Triage Result:", json.dumps(triage, indent=2))

    spec = generate_spec(triage)
    print("Spec Result:", json.dumps(spec, indent=2))

    with open("triage.json", "w", encoding="utf-8") as f:
        json.dump(triage, f, indent=2, ensure_ascii=False)
    with open("spec.json", "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)

