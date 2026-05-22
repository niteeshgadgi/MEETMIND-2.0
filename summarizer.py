import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def summarize_transcript(transcript_text: str, meeting_name: str) -> dict:
    """
    Takes raw meeting transcript text and returns a structured summary dict.
    Uses Groq llama-3.1-8b-instant (fast + cheap = CascadeFlow 'simple task' route).
    Falls back to a safe error dict if anything goes wrong.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("[summarizer] ERROR: GROQ_API_KEY not found in .env")
        return _error_summary(transcript_text, "GROQ_API_KEY missing")

    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an expert meeting analyst. "
        "Extract ONLY information explicitly stated in the transcript. "
        "Never infer or add context not present in the text."
    )

    user_prompt = f"""Analyze this meeting transcript and return a JSON object with EXACTLY these keys:
- "decisions": list of strings — decisions that were confirmed/agreed during the meeting
- "blockers": list of strings — open questions, blockers, or unresolved issues mentioned
- "action_items": list of strings — specific tasks assigned, include the owner's name if mentioned
- "people": list of strings — names of people mentioned in the transcript
- "summary": string — one paragraph (3-5 sentences) summarizing what happened

Return ONLY valid JSON. No markdown, no explanation, no preamble. Just the JSON object.

Transcript:
{transcript_text}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=1024
        )

        raw_text = response.choices[0].message.content.strip()

        # Strip markdown fences if the model wrapped in ```json
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`").strip()
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()

        parsed = json.loads(raw_text)

        # Ensure all keys exist even if model skipped one
        result = {
            "decisions":    parsed.get("decisions", []),
            "blockers":     parsed.get("blockers", []),
            "action_items": parsed.get("action_items", []),
            "people":       parsed.get("people", []),
            "summary":      parsed.get("summary", ""),
            "model_used":   "llama-3.1-8b-instant",
            "cost":         "$0.001",
            "routed_by":    "CascadeFlow (simple task)"
        }

        print(f"[summarizer] ✓ '{meeting_name}' summarized — {len(result['decisions'])} decisions, {len(result['blockers'])} blockers")
        return result

    except json.JSONDecodeError as e:
        print(f"[summarizer] JSON parse failed: {e}. Returning raw text in summary.")
        return _error_summary(raw_text, f"JSON parse error: {e}")

    except Exception as e:
        print(f"[summarizer] Groq API call failed: {e}")
        return _error_summary(transcript_text, str(e))


def _error_summary(raw_text: str, error_msg: str) -> dict:
    """Safe fallback when summarization fails."""
    return {
        "decisions":    [],
        "blockers":     [f"Summarization error: {error_msg}"],
        "action_items": [],
        "people":       [],
        "summary":      raw_text[:500] if raw_text else "Could not process transcript.",
        "model_used":   "llama-3.1-8b-instant",
        "cost":         "$0.000",
        "routed_by":    "CascadeFlow (simple task) — FAILED"
    }
