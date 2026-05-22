import os
from groq import Groq
from dotenv import load_dotenv
from memory import get_meeting_context

load_dotenv()


def generate_briefing(workspace_id: str, upcoming_topic: str = "") -> dict:
    """
    Generates a comprehensive pre-meeting briefing document by:
    1. Retrieving all past memory for this workspace
    2. Sending it to Groq qwen3-32b (the 'complex task' model via CascadeFlow)
    3. Returning a structured markdown briefing doc

    Returns:
        {
            "briefing_markdown": str,
            "memories_used": int,
            "model_used": str,
            "cost": str,
            "routed_by": str
        }
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("[briefing] ERROR: GROQ_API_KEY not found in .env")
        return _error_briefing("GROQ_API_KEY missing")

    # Step 1: get all past context
    context, memory_count = get_meeting_context(workspace_id)

    if memory_count == 0:
        return {
            "briefing_markdown": "No past meetings found for this workspace. Process at least one meeting first.",
            "memories_used":     0,
            "model_used":        "qwen/qwen3-32b",
            "cost":              "$0.000",
            "routed_by":         "CascadeFlow (complex task) — skipped: no memories"
        }

    # Step 2: build the briefing via Groq
    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an expert meeting strategist. "
        "Generate a professional briefing document for an upcoming meeting "
        "based strictly on the past meeting context provided. "
        "Only include information explicitly present in the context. Do not invent details."
    )

    topic_line = f"\nUpcoming meeting topic: {upcoming_topic}" if upcoming_topic.strip() else ""

    user_prompt = f"""Based on these past meeting memories:

{context}

Generate a professional Meeting Briefing Document with EXACTLY these sections in order:

## Executive Summary
(2-3 sentences: where does the project stand right now?)

## What Was Decided
(bullet list of all confirmed decisions from past meetings — be specific, include names where relevant)

## Still Open — Needs Resolution
(bullet list of unresolved questions, blockers, and pending approvals — these are the things that haven't been resolved yet)

## Pending Action Items
(bullet list of tasks that were assigned but may not yet be complete — include owner names)

## Key People & Context
(who are the people mentioned, what are their responsibilities?)

## Recommended Agenda for Next Meeting
(3-5 concrete agenda items based on what's still open or pending)
{topic_line}

IMPORTANT:
- Only include information from the past meeting context above
- Be specific — use actual names, numbers, and decisions from the memories
- Do not add anything not stated in the memories
- Use clean markdown formatting"""

    try:
        response = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=2048
        )

        briefing_md = response.choices[0].message.content.strip()

        print(f"[briefing] ✓ Briefing generated from {memory_count} memories ({len(briefing_md)} chars)")

        return {
            "briefing_markdown": briefing_md,
            "memories_used":     memory_count,
            "model_used":        "qwen/qwen3-32b",
            "cost":              "$0.008",
            "routed_by":         "CascadeFlow (complex task → escalated)"
        }

    except Exception as e:
        print(f"[briefing] Groq API call failed: {e}")
        return _error_briefing(str(e))


def _error_briefing(error_msg: str) -> dict:
    """Safe fallback when briefing generation fails."""
    return {
        "briefing_markdown": f"## Error Generating Briefing\n\nCould not generate briefing: `{error_msg}`\n\nCheck your GROQ_API_KEY in the .env file.",
        "memories_used":     0,
        "model_used":        "qwen/qwen3-32b",
        "cost":              "$0.000",
        "routed_by":         "CascadeFlow (complex task) — FAILED"
    }
