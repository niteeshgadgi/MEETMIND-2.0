import os
import json
import uuid
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

LOCAL_MEMORY_FILE = "memories.json"


# ══════════════════════════════════════════════════════════════════════════════
# LOCAL STORAGE HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _load_local_memories() -> list:
    """Read memories.json. Returns empty list if file missing or corrupt."""
    path = Path(LOCAL_MEMORY_FILE)
    if not path.exists():
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[memory] Could not read {LOCAL_MEMORY_FILE}: {e}")
        return []


def _save_local_memories(memories_list: list) -> None:
    """Write the full memories list back to memories.json."""
    try:
        with open(LOCAL_MEMORY_FILE, "w") as f:
            json.dump(memories_list, f, indent=2)
    except IOError as e:
        print(f"[memory] Could not write {LOCAL_MEMORY_FILE}: {e}")


def _format_summary_as_text(summary_dict: dict, meeting_name: str) -> str:
    """Convert a summary dict into a readable text block for storage."""
    lines = [f"MEETING: {meeting_name}"]

    if summary_dict.get("decisions"):
        lines.append("DECISIONS:")
        for d in summary_dict["decisions"]:
            lines.append(f"  - {d}")

    if summary_dict.get("blockers"):
        lines.append("BLOCKERS:")
        for b in summary_dict["blockers"]:
            lines.append(f"  - {b}")

    if summary_dict.get("action_items"):
        lines.append("ACTION ITEMS:")
        for a in summary_dict["action_items"]:
            lines.append(f"  - {a}")

    if summary_dict.get("people"):
        lines.append(f"PEOPLE: {', '.join(summary_dict['people'])}")

    if summary_dict.get("summary"):
        lines.append(f"SUMMARY: {summary_dict['summary']}")

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def store_meeting_memory(summary_dict: dict, meeting_name: str, workspace_id: str) -> dict:
    """
    Stores a meeting summary.
    1. Tries Hindsight API first.
    2. Falls back to local memories.json if API fails or keys are missing.

    Returns:
        { "success": bool, "storage": "hindsight" | "local", "memory_id": str }
    """
    api_key     = os.getenv("HINDSIGHT_API_KEY")
    pipeline_id = os.getenv("HINDSIGHT_PIPELINE_ID")
    memory_id   = str(uuid.uuid4())[:8]
    text_block  = _format_summary_as_text(summary_dict, meeting_name)

    # ── Try Hindsight ──────────────────────────────────────────────────────────
    if api_key and pipeline_id:
        try:
            resp = requests.post(
                "https://api.hindsight.vectorize.io/v1/memories",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type":  "application/json"
                },
                json={
                    "pipeline_id": pipeline_id,
                    "text":        text_block,
                    "metadata": {
                        "meeting_name": meeting_name,
                        "workspace_id": workspace_id
                    }
                },
                timeout=10
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                memory_id = data.get("id", memory_id)
                print(f"[memory] ✓ Stored to Hindsight — id: {memory_id}")
                return {"success": True, "storage": "hindsight", "memory_id": memory_id}
            else:
                print(f"[memory] Hindsight returned {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            print(f"[memory] Hindsight API error: {e} — falling back to local")
    else:
        print("[memory] Hindsight keys not set — using local storage")

    # ── Local fallback ─────────────────────────────────────────────────────────
    memories = _load_local_memories()
    entry = {
        "memory_id":    memory_id,
        "meeting_name": meeting_name,
        "workspace_id": workspace_id,
        "text":         text_block,
        "summary":      summary_dict,
        "stored_at":    datetime.utcnow().isoformat()
    }
    memories.append(entry)
    _save_local_memories(memories)
    print(f"[memory] ✓ Stored locally — id: {memory_id}  ({len(memories)} total)")
    return {"success": True, "storage": "local", "memory_id": memory_id}


def get_meeting_context(workspace_id: str) -> tuple:
    """
    Retrieves all past meeting context for a workspace.
    1. Tries Hindsight recall API first.
    2. Falls back to local memories.json.

    Returns:
        (context_string, memory_count)
        context_string — all memory texts joined by separators
        memory_count   — integer count of memories found
    """
    api_key     = os.getenv("HINDSIGHT_API_KEY")
    pipeline_id = os.getenv("HINDSIGHT_PIPELINE_ID")

    # ── Try Hindsight recall ───────────────────────────────────────────────────
    if api_key and pipeline_id:
        try:
            resp = requests.post(
                "https://api.hindsight.vectorize.io/v1/recall",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type":  "application/json"
                },
                json={
                    "pipeline_id": pipeline_id,
                    "query":       "meeting decisions blockers action items people",
                    "filter":      {"workspace_id": workspace_id},
                    "top_k":       20
                },
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                # Hindsight returns results in a "results" or "memories" list
                items = data.get("results", data.get("memories", []))
                if items:
                    texts = [item.get("text", "") for item in items if item.get("text")]
                    context = "\n\n---\n\n".join(texts)
                    print(f"[memory] ✓ Retrieved {len(texts)} memories from Hindsight")
                    return context, len(texts)
                else:
                    print("[memory] Hindsight returned 0 results — trying local")
            else:
                print(f"[memory] Hindsight recall returned {resp.status_code}")
        except Exception as e:
            print(f"[memory] Hindsight recall error: {e} — falling back to local")

    # ── Local fallback ─────────────────────────────────────────────────────────
    memories = _load_local_memories()
    workspace_memories = [m for m in memories if m.get("workspace_id") == workspace_id]

    if not workspace_memories:
        print(f"[memory] No local memories found for workspace '{workspace_id}'")
        return "", 0

    texts   = [m.get("text", "") for m in workspace_memories if m.get("text")]
    context = "\n\n---\n\n".join(texts)
    print(f"[memory] ✓ Retrieved {len(texts)} memories from local storage")
    return context, len(texts)
