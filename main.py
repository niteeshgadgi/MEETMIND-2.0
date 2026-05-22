"""
main.py — MeetMind backend entry point.

This file is the ONLY module app.py imports from.
It exposes clean public functions and hides all the internals.
"""

import json
from datetime import datetime
from pathlib import Path

from summarizer import summarize_transcript
from memory import store_meeting_memory, get_meeting_context, _load_local_memories
from briefing import generate_briefing as _generate_briefing

CASCADEFLOW_LOG_FILE = "cascadeflow_log.json"


# ── Internal: CascadeFlow audit log ───────────────────────────────────────────

def _log_cascadeflow_decision(task_type: str, model_used: str, cost: str) -> None:
    """Append a routing decision to cascadeflow_log.json."""
    path = Path(CASCADEFLOW_LOG_FILE)
    logs = []
    if path.exists():
        try:
            with open(path, "r") as f:
                logs = json.load(f)
        except Exception:
            logs = []

    logs.append({
        "timestamp":  datetime.utcnow().isoformat(),
        "task_type":  task_type,
        "model_used": model_used,
        "cost":       cost
    })

    with open(path, "w") as f:
        json.dump(logs, f, indent=2)


def get_cascadeflow_log() -> list:
    """Return all CascadeFlow routing decisions."""
    path = Path(CASCADEFLOW_LOG_FILE)
    if not path.exists():
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return []


# ── Public API (imported by app.py) ───────────────────────────────────────────

def process_meeting(transcript_text: str, meeting_name: str, workspace_id: str) -> dict:
    """
    Full pipeline for a single meeting:
      1. Summarize transcript → structured dict
      2. Store summary to memory (Hindsight or local)
      3. Log the CascadeFlow routing decision
      4. Return combined result

    Returns:
        {
            "summary":        dict (decisions, blockers, action_items, people, summary, ...),
            "storage_result": dict (success, storage, memory_id)
        }
    """
    print(f"\n[main] Processing meeting: '{meeting_name}' for workspace '{workspace_id}'")

    # Step 1: Summarize
    summary = summarize_transcript(transcript_text, meeting_name)

    # Step 2: Store
    storage_result = store_meeting_memory(summary, meeting_name, workspace_id)

    # Step 3: Log routing decision
    _log_cascadeflow_decision(
        task_type  = "transcript_summarization",
        model_used = summary.get("model_used", "llama-3.1-8b-instant"),
        cost       = summary.get("cost", "$0.001")
    )

    print(f"[main] ✓ Meeting processed. Storage: {storage_result.get('storage')} — id: {storage_result.get('memory_id')}")
    return {
        "summary":        summary,
        "storage_result": storage_result
    }


def get_briefing(workspace_id: str, upcoming_topic: str = "") -> dict:
    """
    Generate a cross-session briefing document from all past memories.

    Returns the briefing dict from briefing.py, plus logs the routing decision.
    """
    print(f"\n[main] Generating briefing for workspace '{workspace_id}'")

    result = _generate_briefing(workspace_id, upcoming_topic)

    _log_cascadeflow_decision(
        task_type  = "cross_session_briefing",
        model_used = result.get("model_used", "qwen/qwen3-32b"),
        cost       = result.get("cost", "$0.008")
    )

    return result


def get_memory_count(workspace_id: str) -> int:
    """Return the number of memories stored for a workspace."""
    _, count = get_meeting_context(workspace_id)
    return count


def get_all_memories_display(workspace_id: str) -> list:
    """
    Returns a list of raw memory entries for a workspace.
    Used by the Memory Log page in app.py.
    Falls back to local storage (works even without Hindsight).
    """
    memories = _load_local_memories()
    return [m for m in memories if m.get("workspace_id") == workspace_id]


# ══════════════════════════════════════════════════════════════════════════════
# SELF-TEST — run with: python main.py
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("MeetMind — End-to-End Self Test")
    print("=" * 60)

    TEST_WORKSPACE = "selftest-workspace"

    TRANSCRIPT_1 = """
    Maya: We need to lock in our tech stack today.
    Rohan: I recommend React for frontend and Python FastAPI for backend.
    Maya: Agreed. That's decided. Rohan, you own the infrastructure setup by Friday.
    Priya: I'll have the design wireframes ready by next Wednesday.
    Maya: Pricing — we're going with $29 per user per month. That's confirmed.
    Rohan: One blocker — legal still hasn't signed off on the data processing agreement. Nothing can go public without it.
    Maya: Noted. That's on the critical path. Launch target is 8 weeks from today.
    """

    TRANSCRIPT_2 = """
    Sam: Infrastructure from last week is done. But we hit a problem — Mixpanel has API rate limits that would cap us at peak traffic.
    Maya: What do we do?
    Sam: Switch to Amplitude. No rate limit issues at our scale.
    Maya: Decision — we use Amplitude. Sam, negotiate pricing with them this week.
    Priya: Wireframes are complete. Team approved the dashboard home screen last session.
    Maya: Legal DPA is still unsigned. It's now blocking the public launch. This is our critical path item.
    Sam: Can we soft-launch to beta users in the meantime?
    Maya: Good idea — let's decide that next week once we see the legal timeline.
    """

    print("\n── Test 1: Process Week 1 meeting ─────────────────────────")
    r1 = process_meeting(TRANSCRIPT_1, "Week 1 — Sprint Kickoff", TEST_WORKSPACE)
    print("  Decisions:", r1["summary"]["decisions"])
    print("  Blockers:", r1["summary"]["blockers"])
    print("  Storage:", r1["storage_result"]["storage"])

    print("\n── Test 2: Process Week 2 meeting ─────────────────────────")
    r2 = process_meeting(TRANSCRIPT_2, "Week 2 — Infrastructure Review", TEST_WORKSPACE)
    print("  Decisions:", r2["summary"]["decisions"])
    print("  Blockers:", r2["summary"]["blockers"])
    print("  Storage:", r2["storage_result"]["storage"])

    print("\n── Test 3: Memory count ────────────────────────────────────")
    count = get_memory_count(TEST_WORKSPACE)
    print(f"  Memories found: {count}")
    assert count >= 2, f"FAIL: Expected at least 2 memories, got {count}"
    print("  ✓ PASS")

    print("\n── Test 4: Generate briefing ───────────────────────────────")
    briefing = get_briefing(TEST_WORKSPACE, "Week 3 planning")
    print(f"  Memories used: {briefing['memories_used']}")
    print(f"  Model: {briefing['model_used']}")
    print(f"  Cost: {briefing['cost']}")
    print("\n  BRIEFING PREVIEW (first 600 chars):")
    print("  " + briefing["briefing_markdown"][:600].replace("\n", "\n  "))
    assert briefing["memories_used"] >= 2, "FAIL: Briefing should use at least 2 memories"
    print("\n  ✓ PASS")

    print("\n── Test 5: CascadeFlow log ─────────────────────────────────")
    logs = get_cascadeflow_log()
    print(f"  Log entries: {len(logs)}")
    for entry in logs[-3:]:
        print(f"  {entry['task_type']} → {entry['model_used']} | {entry['cost']}")

    print("\n" + "=" * 60)
    print("✓ All tests passed. Backend is ready.")
    print("=" * 60)
