import streamlit as st
import time

# ── Page config (must be FIRST streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="MeetMind — Team Memory",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=DM+Mono:wght@300;400;500&display=swap');

    /* ── Base ── */
    .stApp { background-color: #090912; font-family: 'Syne', sans-serif; }
    .stApp > header { background-color: transparent !important; }
    * { font-family: 'Syne', sans-serif !important; }
    
    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #0f0f1e !important;
        border-right: 1px solid #1e1e35 !important;
    }
    [data-testid="stSidebar"] * { color: #c8c8e0 !important; }

    /* ── Text ── */
    .stApp, .stMarkdown, p { color: #d8d8ee !important; }
    h1, h2, h3, h4 { 
        color: #eeeeff !important; 
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }
    label { color: #9999bb !important; font-size: 13px !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #4f35a0 0%, #2d1d6e 100%) !important;
        color: #eeeeff !important;
        border: 1px solid #6040c0 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-family: 'Syne', sans-serif !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
        padding: 0.55rem 1.5rem !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 24px rgba(79,53,160,0.45) !important;
        border-color: #8060e0 !important;
    }
    .stButton > button:active { transform: translateY(0px) !important; }

    /* ── Inputs ── */
    .stTextArea textarea, .stTextInput input {
        background-color: #0f0f1e !important;
        color: #d8d8ee !important;
        border: 1px solid #1e1e38 !important;
        border-radius: 6px !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 13px !important;
        transition: border-color 0.2s !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #4f35a0 !important;
        box-shadow: 0 0 0 2px rgba(79,53,160,0.2) !important;
    }

    /* ── Selectbox / Radio ── */
    .stRadio label { color: #9999bb !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: #d8d8ee !important; }
    [data-baseweb="select"] div { 
        background-color: #0f0f1e !important;
        border-color: #1e1e38 !important;
        color: #d8d8ee !important;
    }

    /* ── Metrics ── */
    [data-testid="metric-container"] {
        background-color: #0f0f1e !important;
        border: 1px solid #1e1e38 !important;
        border-radius: 8px !important;
        padding: 1rem 1.2rem !important;
    }
    [data-testid="metric-container"] label { color: #6666aa !important; font-size: 11px !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #9975dd !important;
        font-size: 22px !important;
        font-weight: 600 !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background-color: #0f0f1e !important;
        border: 1px solid #1e1e38 !important;
        border-radius: 6px !important;
        color: #d8d8ee !important;
    }
    .streamlit-expanderContent {
        background-color: #0c0c18 !important;
        border: 1px solid #1e1e38 !important;
        border-top: none !important;
    }

    /* ── Alerts ── */
    .stSuccess {
        background-color: rgba(40,180,100,0.08) !important;
        border-left: 3px solid #28b464 !important;
        border-radius: 4px !important;
    }
    .stError {
        background-color: rgba(200,50,50,0.08) !important;
        border-left: 3px solid #c83232 !important;
    }
    .stInfo {
        background-color: rgba(79,53,160,0.1) !important;
        border-left: 3px solid #4f35a0 !important;
    }
    .stWarning {
        background-color: rgba(200,140,30,0.08) !important;
        border-left: 3px solid #c88c1e !important;
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #6040c0 !important; }

    /* ── Dividers ── */
    hr { border-color: #1a1a30 !important; margin: 1.5rem 0 !important; }

    /* ── Hide Streamlit chrome ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ── Code / mono ── */
    code { 
        background: #0f0f1e !important;
        color: #9975dd !important;
        border: 1px solid #1e1e38 !important;
        border-radius: 3px !important;
        font-family: 'DM Mono', monospace !important;
        padding: 1px 5px !important;
    }

    /* ── Tabs (used in Memory Log) ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0f0f1e !important;
        border-bottom: 1px solid #1e1e38 !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #6666aa !important;
        border-radius: 0 !important;
        padding: 0.6rem 1.2rem !important;
    }
    .stTabs [aria-selected="true"] {
        color: #c0a0ff !important;
        border-bottom: 2px solid #6040c0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Session state init ─────────────────────────────────────────────────────────
if "processed_meetings" not in st.session_state:
    st.session_state.processed_meetings = []
if "cascadeflow_log" not in st.session_state:
    st.session_state.cascadeflow_log = []
if "last_briefing" not in st.session_state:
    st.session_state.last_briefing = None
if "backend_ready" not in st.session_state:
    st.session_state.backend_ready = False


# ── Try to import backend ─────────────────────────────────────────────────────
try:
    from main import process_meeting, get_briefing, get_memory_count, get_all_memories_display
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False


# ── Helper: route tag pill ─────────────────────────────────────────────────────
def route_pill(model: str, task: str, cost: str) -> str:
    return f"""
    <div style="display:inline-flex; align-items:center; gap:8px; 
                background:#0f0f1e; border:1px solid #1e1e38; 
                border-radius:20px; padding:5px 12px; margin-top:10px;">
        <span style="width:7px;height:7px;background:#6040c0;border-radius:50%;display:inline-block;"></span>
        <span style="font-family:'DM Mono',monospace; font-size:11px; color:#8866cc;">
            CascadeFlow → {model}
        </span>
        <span style="color:#333360; font-size:11px;">|</span>
        <span style="font-family:'DM Mono',monospace; font-size:11px; color:#555588;">{task}</span>
        <span style="color:#333360; font-size:11px;">|</span>
        <span style="font-family:'DM Mono',monospace; font-size:11px; color:#28b464;">{cost}</span>
    </div>"""


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding: 1.2rem 0 0.8rem;">
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:26px;">🧠</span>
            <div>
                <div style="color:#eeeeff; font-size:18px; font-weight:700; letter-spacing:-0.02em;">MeetMind</div>
                <div style="color:#555588; font-size:11px; font-family:'DM Mono',monospace;">v1.0 · team memory</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Backend status
    if BACKEND_AVAILABLE:
        st.markdown("""<div style="display:flex;align-items:center;gap:6px;margin-bottom:12px;">
            <span style="width:7px;height:7px;background:#28b464;border-radius:50%;display:inline-block;"></span>
            <span style="font-size:12px;color:#28b464;font-family:'DM Mono',monospace;">backend connected</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="display:flex;align-items:center;gap:6px;margin-bottom:12px;">
            <span style="width:7px;height:7px;background:#c88c1e;border-radius:50%;display:inline-block;"></span>
            <span style="font-size:12px;color:#c88c1e;font-family:'DM Mono',monospace;">UI preview mode</span>
        </div>""", unsafe_allow_html=True)

    # Workspace
    st.markdown("<div style='font-size:11px;color:#555588;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;'>Workspace</div>", unsafe_allow_html=True)
    workspace_id = st.text_input(
        "workspace_id",
        value="demo-team-alpha",
        label_visibility="collapsed",
        key="workspace_input"
    )

    st.markdown("---")

    # Navigation
    st.markdown("<div style='font-size:11px;color:#555588;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio(
        "nav",
        ["⚡  Process Meeting", "📋  Generate Briefing", "🗂  Memory Log"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Demo mode
    st.markdown("<div style='font-size:11px;color:#555588;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;'>Demo</div>", unsafe_allow_html=True)
    
    if st.button("🎬  Load Demo Data", use_container_width=True):
        from demo_data import DEMO_TRANSCRIPTS, DEMO_WORKSPACE
        if BACKEND_AVAILABLE:
            with st.spinner("Processing 3 weeks of meetings..."):
                for week_key, week_data in DEMO_TRANSCRIPTS.items():
                    result = process_meeting(
                        week_data["transcript"],
                        week_data["name"],
                        DEMO_WORKSPACE
                    )
                    st.session_state.processed_meetings.append({
                        "name": week_data["name"],
                        "summary": result["summary"]
                    })
                    st.session_state.cascadeflow_log.append({
                        "meeting": week_data["name"],
                        "model": "llama-3.1-8b-instant",
                        "task": "summarization",
                        "cost": "$0.001"
                    })
            st.success("3 meetings loaded!")
            st.rerun()
        else:
            # Offline demo — inject fake summaries so UI renders
            from demo_data import DEMO_TRANSCRIPTS, DEMO_WORKSPACE
            fake_summaries = [
                {
                    "decisions": ["Use React + FastAPI", "Pricing: $29/month", "8-week launch target"],
                    "blockers": ["Legal DPA not yet signed", "Analytics provider undecided"],
                    "action_items": ["Rohan: infra by Friday", "Priya: wireframes by Wednesday", "Follow up legal DPA"],
                    "people": ["Maya", "Rohan", "Priya"],
                    "summary": "Team kicked off Q3 sprint. Agreed on React+FastAPI stack and $29/month pricing. Launch target is 8 weeks. Legal DPA is a blocking dependency.",
                    "model_used": "llama-3.1-8b-instant",
                    "cost": "$0.001",
                    "routed_by": "CascadeFlow (simple task)"
                },
                {
                    "decisions": ["Switch from Mixpanel to Amplitude", "Sam to negotiate Amplitude pricing"],
                    "blockers": ["Legal DPA still pending — now on critical path"],
                    "action_items": ["Rohan: integrate Amplitude by Thursday", "Sam: close Amplitude deal"],
                    "people": ["Maya", "Rohan", "Priya", "Sam"],
                    "summary": "Rohan flagged Mixpanel rate limit issues. Team switched to Amplitude. Legal DPA still unresolved and now blocks launch.",
                    "model_used": "llama-3.1-8b-instant",
                    "cost": "$0.001",
                    "routed_by": "CascadeFlow (simple task)"
                },
                {
                    "decisions": ["Amplitude deal closed at $800/month", "Soft launch with 12 beta companies", "Mobile responsive adds 3 days"],
                    "blockers": ["Legal DPA awaiting signature (3-5 days)"],
                    "action_items": ["Priya: beta onboarding emails by Wednesday", "Rohan: integration by Monday", "Sam: beta agreement draft"],
                    "people": ["Maya", "Rohan", "Priya", "Sam"],
                    "summary": "Amplitude deal closed at $800/mo. Team decided to soft launch with 12 beta companies while waiting for legal. Mobile responsive adds 3 days.",
                    "model_used": "llama-3.1-8b-instant",
                    "cost": "$0.001",
                    "routed_by": "CascadeFlow (simple task)"
                }
            ]
            for i, week_data in enumerate(DEMO_TRANSCRIPTS.values()):
                st.session_state.processed_meetings.append({
                    "name": week_data["name"],
                    "summary": fake_summaries[i]
                })
                st.session_state.cascadeflow_log.append({
                    "meeting": week_data["name"],
                    "model": "llama-3.1-8b-instant",
                    "task": "summarization",
                    "cost": "$0.001"
                })
            st.success("3 demo meetings loaded! (UI preview)")
            st.rerun()

    meetings_count = len(st.session_state.processed_meetings)
    if meetings_count > 0:
        st.markdown(f"""
        <div style="text-align:center; padding:8px; background:#0f0f1e; 
                    border:1px solid #1e1e38; border-radius:6px; margin-top:8px;">
            <span style="font-family:'DM Mono',monospace; font-size:11px; color:#9975dd;">
                {meetings_count} meeting{'s' if meetings_count != 1 else ''} in memory
            </span>
        </div>""", unsafe_allow_html=True)

    # Bottom badge
    st.markdown("---")
    st.markdown("""
    <div style="font-size:10px; color:#333355; text-align:center; line-height:1.8;">
        Powered by<br>
        <span style="color:#6655aa;">Hindsight Memory</span> · 
        <span style="color:#4466aa;">CascadeFlow</span> · 
        <span style="color:#446688;">Groq</span>
    </div>
    """, unsafe_allow_html=True)


# ── Main header ────────────────────────────────────────────────────────────────
col_logo, col_status = st.columns([4, 1])
with col_logo:
    st.markdown("""
    <div style="padding: 0.5rem 0 0.2rem;">
        <h1 style="margin:0; font-size:26px; font-weight:700; letter-spacing:-0.03em; color:#eeeeff;">
            Your team's institutional memory
        </h1>
        <p style="margin:4px 0 0; font-size:13px; color:#555588; font-family:'DM Mono',monospace;">
            paste transcript → extract → remember → brief
        </p>
    </div>
    """, unsafe_allow_html=True)
with col_status:
    status_label = "● connected" if BACKEND_AVAILABLE else "◌ preview"
    status_color = "#28b464" if BACKEND_AVAILABLE else "#c88c1e"
    st.markdown(f"""
    <div style="text-align:right; padding-top:0.8rem;">
        <span style="font-family:'DM Mono',monospace; font-size:11px; color:{status_color};">
            {status_label}
        </span>
    </div>""", unsafe_allow_html=True)

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Process Meeting
# ══════════════════════════════════════════════════════════════════════════════
if page == "⚡  Process Meeting":
    st.markdown("## ⚡ Process New Meeting")
    st.markdown("<p style='color:#666688; font-size:14px; margin-top:-8px;'>Paste a transcript. MeetMind extracts decisions, blockers, action items and stores them as memory.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        meeting_name = st.text_input(
            "Meeting name",
            placeholder="e.g. Week 4 — Backend Review",
            key="meeting_name_input"
        )
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-family:DM Mono,monospace; font-size:11px; color:#555588; padding-top:8px;'>workspace: <span style='color:#9975dd;'>{workspace_id}</span></div>", unsafe_allow_html=True)

    transcript = st.text_area(
        "Meeting transcript",
        placeholder="Paste your meeting transcript here...\n\nExample:\nMaya: We need to decide on the launch date.\nRohan: I think next Friday works.\nMaya: Agreed — Friday it is. Rohan owns the release.",
        height=300,
        key="transcript_input"
    )

    process_clicked = st.button("⚡ Process & Remember", use_container_width=True, key="process_btn")

    if process_clicked:
        if not transcript.strip():
            st.error("Please paste a meeting transcript first.")
        elif not meeting_name.strip():
            st.error("Please give this meeting a name.")
        else:
            with st.spinner("🧠 Extracting insights and storing to memory..."):
                if BACKEND_AVAILABLE:
                    try:
                        result = process_meeting(transcript, meeting_name, workspace_id)
                        summary = result["summary"]
                        storage = result.get("storage_result", {})
                        storage_type = storage.get("storage", "local")
                    except Exception as e:
                        st.error(f"Backend error: {e}")
                        st.stop()
                else:
                    # Preview mode — simulate a result
                    time.sleep(1.5)
                    summary = {
                        "decisions": ["Decision extracted from transcript", "Another key decision made"],
                        "blockers": ["Open question or blocker identified"],
                        "action_items": ["Owner: task to be completed by date"],
                        "people": ["Person A", "Person B"],
                        "summary": f"This is a simulated summary for '{meeting_name}'. Connect the backend to see real AI extraction.",
                        "model_used": "llama-3.1-8b-instant",
                        "cost": "$0.001",
                        "routed_by": "CascadeFlow (simple task)"
                    }
                    storage_type = "local (preview)"

            st.success(f"✅ Memory stored · {storage_type}")

            # Store in session
            st.session_state.processed_meetings.append({
                "name": meeting_name,
                "summary": summary
            })
            st.session_state.cascadeflow_log.append({
                "meeting": meeting_name,
                "model": summary.get("model_used", "llama-3.1-8b-instant"),
                "task": "summarization",
                "cost": summary.get("cost", "$0.001")
            })

            # Summary display
            st.markdown("### Extracted Summary")
            c1, c2, c3, c4 = st.columns(4)

            def render_list_col(col, title, items, accent):
                with col:
                    st.markdown(f"""
                    <div style="background:#0f0f1e; border:1px solid #1e1e38; border-radius:8px; 
                                padding:1rem; min-height:140px;">
                        <div style="font-size:10px; text-transform:uppercase; letter-spacing:0.1em; 
                                    color:{accent}; margin-bottom:10px; font-family:'DM Mono',monospace;">
                            {title}
                        </div>
                        {''.join([f'<div style="font-size:12px; color:#c0c0d8; padding:3px 0; border-bottom:1px solid #141428;">· {item}</div>' for item in (items or ["None identified"])]) }
                    </div>""", unsafe_allow_html=True)

            render_list_col(c1, "✓ Decisions", summary.get("decisions", []), "#28b464")
            render_list_col(c2, "⚠ Blockers", summary.get("blockers", []), "#c88c1e")
            render_list_col(c3, "→ Action Items", summary.get("action_items", []), "#4488cc")
            render_list_col(c4, "◎ People", summary.get("people", []), "#9975dd")

            # Summary paragraph
            st.markdown(f"""
            <div style="background:#0c0c18; border:1px solid #1e1e38; border-left:3px solid #4f35a0;
                        border-radius:4px; padding:1rem 1.2rem; margin-top:1rem;">
                <div style="font-size:10px; text-transform:uppercase; letter-spacing:0.08em; 
                            color:#555588; margin-bottom:6px; font-family:'DM Mono',monospace;">Summary</div>
                <div style="font-size:13px; color:#d0d0e8; line-height:1.6;">{summary.get("summary", "")}</div>
            </div>""", unsafe_allow_html=True)

            # Route pill
            st.markdown(route_pill(
                summary.get("model_used", "llama-3.1-8b-instant"),
                "simple task",
                summary.get("cost", "$0.001")
            ), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Generate Briefing
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋  Generate Briefing":
    st.markdown("## 📋 Generate Meeting Briefing")
    st.markdown("<p style='color:#666688; font-size:14px; margin-top:-8px;'>Synthesizes context from all past meetings into a single pre-meeting brief.</p>", unsafe_allow_html=True)

    upcoming_topic = st.text_input(
        "Upcoming meeting topic (optional)",
        placeholder="e.g. Q3 retrospective and Q4 planning",
        key="upcoming_topic"
    )

    briefing_clicked = st.button("📋 Generate Briefing Doc", use_container_width=True, key="briefing_btn")

    if briefing_clicked:
        count_check = len(st.session_state.processed_meetings)
        if count_check == 0 and not BACKEND_AVAILABLE:
            st.warning("Load demo data first (sidebar) or process at least one meeting.")
        else:
            with st.spinner("🧠 Retrieving memories and synthesizing briefing..."):
                if BACKEND_AVAILABLE:
                    try:
                        result = get_briefing(workspace_id, upcoming_topic)
                    except Exception as e:
                        st.error(f"Backend error: {e}")
                        st.stop()
                else:
                    time.sleep(2)
                    meetings_used = len(st.session_state.processed_meetings)
                    result = {
                        "briefing_markdown": f"""## Executive Summary
The product team is in active development of a B2B analytics dashboard. Core technical decisions have been made (React + FastAPI, Amplitude for analytics) and a soft beta launch is planned while legal finalizes the data processing agreement.

## What Was Decided
- Tech stack: React frontend + FastAPI backend
- Pricing: $29/user/month
- Analytics: Amplitude ($800/month, 2M events included — deal closed by Sam)
- Launch approach: Soft launch with 12 beta companies while legal DPA is finalized
- Mobile responsive version added to scope (+3 days)

## Still Open — Needs Resolution
- Legal DPA: sent for signature, awaiting 3-5 business days response
- Webhook retry logic: Rohan flagged edge cases, needs resolution before full launch
- Public launch blocked until DPA is signed

## Pending Action Items
- **Priya**: Beta onboarding email sequence for 12 companies (due Wednesday)
- **Rohan**: Complete Amplitude integration (due Monday, extended due to mobile scope)
- **Sam**: Draft beta user agreement language

## Key People & Context
- **Maya** (Product Manager): Decision authority, owns legal follow-up and timeline
- **Rohan** (Lead Engineer): Infrastructure, Amplitude integration, webhook logic
- **Priya** (Designer): Wireframes complete, owns beta onboarding emails
- **Sam** (Growth): Closed Amplitude deal, owns beta agreement

## Recommended Agenda for Next Meeting
1. Legal DPA status — is it signed? Unblocks public launch
2. Amplitude integration review — Rohan demos 70%→100% completion
3. Beta onboarding email review — Priya presents drafts
4. Webhook retry logic — brief technical discussion to unblock Rohan
5. Mobile responsive timeline check — confirm scope and dates""",
                        "memories_used": meetings_used,
                        "model_used": "qwen/qwen3-32b",
                        "cost": "$0.008",
                        "routed_by": "CascadeFlow (complex task → escalated)"
                    }

            # Log to cascadeflow
            st.session_state.cascadeflow_log.append({
                "meeting": "Briefing generation",
                "model": result.get("model_used", "qwen/qwen3-32b"),
                "task": "complex synthesis",
                "cost": result.get("cost", "$0.008")
            })
            st.session_state.last_briefing = result

    # Render briefing if available
    if st.session_state.last_briefing:
        result = st.session_state.last_briefing
        
        # Metrics row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Memories Used", result.get("memories_used", "—"))
        m2.metric("Model", result.get("model_used", "qwen3-32b").split("/")[-1])
        m3.metric("Cost", result.get("cost", "$0.008"))
        m4.metric("vs GPT-4o", "−94%")

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # Briefing content
        st.markdown("""
        <div style="background:#0c0c18; border:1px solid #1e1e38; border-radius:8px; padding:1.5rem 2rem;">
        """, unsafe_allow_html=True)
        st.markdown(result.get("briefing_markdown", ""), unsafe_allow_html=False)
        st.markdown("</div>", unsafe_allow_html=True)

        # Route pill
        st.markdown(route_pill(
            result.get("model_used", "qwen/qwen3-32b"),
            "complex task · escalated",
            result.get("cost", "$0.008")
        ), unsafe_allow_html=True)

    elif not briefing_clicked:
        # Empty state
        st.markdown("""
        <div style="text-align:center; padding:4rem 1rem; color:#333355;">
            <div style="font-size:48px; margin-bottom:1rem; opacity:0.4;">📋</div>
            <h3 style="color:#555588 !important; font-weight:400 !important;">No briefing generated yet</h3>
            <p style="color:#444466; font-size:14px;">Load demo data or process meetings, then click the button above.</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Memory Log
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗂  Memory Log":
    st.markdown("## 🗂 Team Memory Log")
    st.markdown(f"<p style='color:#666688; font-size:14px; margin-top:-8px;'>Workspace: <code>{workspace_id}</code></p>", unsafe_allow_html=True)

    # Top metrics
    live_count = 0
    if BACKEND_AVAILABLE:
        try:
            live_count = get_memory_count(workspace_id)
        except:
            live_count = len(st.session_state.processed_meetings)
    else:
        live_count = len(st.session_state.processed_meetings)

    lm1, lm2, lm3 = st.columns(3)
    lm1.metric("Total Memories", live_count)
    lm2.metric("Meetings Processed", len(st.session_state.processed_meetings))
    lm3.metric("AI Calls Made", len(st.session_state.cascadeflow_log))

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["  Meeting Memories  ", "  CascadeFlow Audit Trail  "])

    with tab1:
        if not st.session_state.processed_meetings:
            st.markdown("""
            <div style="text-align:center; padding:3rem 1rem;">
                <div style="font-size:42px; margin-bottom:1rem; opacity:0.3;">🧠</div>
                <h3 style="color:#555588 !important; font-weight:400 !important;">No memories yet</h3>
                <p style="color:#444466; font-size:14px; margin:0;">
                    Use "Load Demo Data" in the sidebar, or process a meeting to start building memory.
                </p>
            </div>""", unsafe_allow_html=True)
        else:
            for i, meeting in enumerate(reversed(st.session_state.processed_meetings)):
                summary = meeting["summary"]
                with st.expander(f"🗂  {meeting['name']}", expanded=(i == 0)):
                    ec1, ec2, ec3, ec4 = st.columns(4)

                    def small_list(col, label, items, color):
                        with col:
                            st.markdown(f"<div style='font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:{color};font-family:DM Mono,monospace;margin-bottom:6px;'>{label}</div>", unsafe_allow_html=True)
                            for item in (items or ["—"]):
                                st.markdown(f"<div style='font-size:12px;color:#b0b0cc;padding:2px 0;'>· {item}</div>", unsafe_allow_html=True)

                    small_list(ec1, "Decisions", summary.get("decisions", []), "#28b464")
                    small_list(ec2, "Blockers", summary.get("blockers", []), "#c88c1e")
                    small_list(ec3, "Action Items", summary.get("action_items", []), "#4488cc")
                    small_list(ec4, "People", summary.get("people", []), "#9975dd")

                    if summary.get("summary"):
                        st.markdown(f"""
                        <div style="background:#090912; border-left:2px solid #1e1e38; 
                                    padding:0.7rem 1rem; margin-top:12px; border-radius:3px;">
                            <div style="font-size:12px; color:#9090aa; line-height:1.6;">{summary["summary"]}</div>
                        </div>""", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style="margin-top:8px; font-family:'DM Mono',monospace; font-size:10px; color:#333355;">
                        model: {summary.get('model_used', '—')} · cost: {summary.get('cost', '—')} · {summary.get('routed_by', '—')}
                    </div>""", unsafe_allow_html=True)

    with tab2:
        if not st.session_state.cascadeflow_log:
            st.markdown("<p style='color:#555588; font-size:13px; padding:1rem 0;'>No routing decisions logged yet.</p>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#0c0c18; border:1px solid #1e1e38; border-radius:8px; padding:1rem 1.2rem; margin-bottom:8px;">
                <div style="font-size:10px; text-transform:uppercase; letter-spacing:0.08em; color:#555588; font-family:'DM Mono',monospace; margin-bottom:10px;">
                    Routing Decisions — Newest First
                </div>""", unsafe_allow_html=True)
            
            for log in reversed(st.session_state.cascadeflow_log):
                task_color = "#9975dd" if "complex" in log.get("task", "") else "#4488cc"
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                            padding:8px 0; border-bottom:1px solid #141428;">
                    <div>
                        <span style="font-size:12px; color:#c0c0d8;">{log.get('meeting', '—')}</span>
                        <span style="font-size:10px; color:#555588; font-family:'DM Mono',monospace; margin-left:8px;">
                            → {log.get('model', '—')}
                        </span>
                    </div>
                    <div style="display:flex; gap:12px; align-items:center;">
                        <span style="font-size:10px; color:{task_color}; font-family:'DM Mono',monospace;">
                            {log.get('task', '—')}
                        </span>
                        <span style="font-size:10px; color:#28b464; font-family:'DM Mono',monospace;">
                            {log.get('cost', '—')}
                        </span>
                    </div>
                </div>""", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

            # Cost summary
            total_cost_str = f"${len(st.session_state.cascadeflow_log) * 0.003:.4f}"
            gpt4_equiv = f"${len(st.session_state.cascadeflow_log) * 0.12:.3f}"
            st.markdown(f"""
            <div style="display:flex; gap:16px; margin-top:12px;">
                <div style="background:#0f0f1e; border:1px solid #1e1e38; border-radius:6px; padding:10px 16px; flex:1; text-align:center;">
                    <div style="font-size:10px; color:#555588; font-family:'DM Mono',monospace; margin-bottom:4px;">ACTUAL COST</div>
                    <div style="font-size:18px; color:#28b464; font-weight:600;">{total_cost_str}</div>
                </div>
                <div style="background:#0f0f1e; border:1px solid #1e1e38; border-radius:6px; padding:10px 16px; flex:1; text-align:center;">
                    <div style="font-size:10px; color:#555588; font-family:'DM Mono',monospace; margin-bottom:4px;">GPT-4o EQUIVALENT</div>
                    <div style="font-size:18px; color:#c83232; font-weight:600;">{gpt4_equiv}</div>
                </div>
                <div style="background:#0f0f1e; border:1px solid #1e1e38; border-radius:6px; padding:10px 16px; flex:1; text-align:center;">
                    <div style="font-size:10px; color:#555588; font-family:'DM Mono',monospace; margin-bottom:4px;">SAVED</div>
                    <div style="font-size:18px; color:#9975dd; font-weight:600;">~94%</div>
                </div>
            </div>""", unsafe_allow_html=True)
