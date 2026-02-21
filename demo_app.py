"""
RecruitingOS — Interactive Demo
Run with: streamlit run demo_app.py
"""

import streamlit as st
import pandas as pd
import time
from mock_data import (
    COMPANIES, DECISION_MAKERS, SIGNALS, QUALIFICATIONS,
    CANDIDATES, CANDIDATE_SCORES, DEMO_JOB, DEMO_TRANSCRIPT,
    EMAIL_REPLIES, CRM_STATS, generate_activity_log,
)
from demo_engine import (
    simulate_process_lead,
    simulate_match_candidates,
    simulate_process_transcript,
    simulate_reply_handling,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="RecruitingOS — Demo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------

st.markdown("""
<style>
    /* Header styling */
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #6b7280;
        margin-top: -10px;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Pipeline step styling */
    .step-running {
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        margin: 8px 0;
        background: #eff6ff;
        border-radius: 0 8px 8px 0;
    }
    .step-done {
        border-left: 4px solid #10b981;
        padding: 12px 16px;
        margin: 8px 0;
        background: #ecfdf5;
        border-radius: 0 8px 8px 0;
    }

    /* Activity feed */
    .activity-item {
        padding: 8px 12px;
        border-bottom: 1px solid #f3f4f6;
        font-size: 0.9rem;
    }

    /* Sidebar */
    .css-1d391kg { padding-top: 2rem; }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Pipeline animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .pulsing { animation: pulse 1.5s infinite; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## ⚡ RecruitingOS")
    st.markdown("*AI Recruitment Infrastructure*")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "🔥 Lead Generation Pipeline",
            "👥 Candidate Matching",
            "📞 Call Transcript Processing",
            "📧 Reply Handling",
            "📊 System Architecture",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("##### How This Demo Works")
    st.markdown(
        "This demo uses **simulated data** to show exactly "
        "how the production system operates. Every step you see "
        "mirrors real API calls to Apollo, OpenAI, AirTable, and more."
    )
    st.markdown("---")
    st.caption("Demo v1.0 — No API keys required")


# ---------------------------------------------------------------------------
# Helper: render pipeline steps
# ---------------------------------------------------------------------------

def render_pipeline(generator, speed_multiplier=1.0):
    """Run a pipeline simulation and render each step in real time."""
    steps_container = st.container()
    completed_steps = {}

    for step_num, step_name, status, detail in generator:
        with steps_container:
            if status == "running":
                # Show the running step with spinner
                completed_steps[step_num] = st.empty()
                with completed_steps[step_num]:
                    st.info(f"**Step {step_num}: {step_name}** — Processing...\n\n{detail}")
            elif status == "done":
                # Replace spinner with done
                if step_num in completed_steps:
                    with completed_steps[step_num]:
                        st.success(f"**Step {step_num}: {step_name}** ✓\n\n{detail}")


# ---------------------------------------------------------------------------
# Page: Dashboard
# ---------------------------------------------------------------------------

def page_dashboard():
    st.markdown('<p class="main-title">RecruitingOS</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Recruitment Infrastructure — Live Dashboard</p>', unsafe_allow_html=True)
    st.markdown("")

    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Companies in CRM", f"{CRM_STATS['total_companies']:,}")
    with col2:
        st.metric("Leads This Week", CRM_STATS["leads_this_week"], delta="+12 vs last week")
    with col3:
        st.metric("Hot Leads", CRM_STATS["hot_leads"], delta="+3")
    with col4:
        st.metric("Reply Rate", CRM_STATS["reply_rate"], delta="+2.1%")
    with col5:
        st.metric("Placements (Month)", CRM_STATS["placements_this_month"])

    st.markdown("---")

    # Two columns: Pipeline summary + Activity feed
    left, right = st.columns([1, 1])

    with left:
        st.markdown("### Three Engines Running 24/7")
        st.markdown("")

        # Engine 1
        with st.container(border=True):
            st.markdown("#### 🔥 Engine 1: Find Clients")
            st.markdown(
                "Scans the market for companies showing **buying signals** — "
                "job postings, website visits, LinkedIn engagement. "
                "Enriches, qualifies, and routes them to outreach automatically."
            )
            c1, c2, c3 = st.columns(3)
            c1.metric("Leads/Week", CRM_STATS["leads_this_week"])
            c2.metric("Emails Sent", CRM_STATS["emails_sent"])
            c3.metric("Meetings Booked", CRM_STATS["meetings_booked"])

        st.markdown("")

        # Engine 2
        with st.container(border=True):
            st.markdown("#### 👥 Engine 2: Find Talent")
            st.markdown(
                "When a new job comes in, the system searches your CRM and external "
                "databases, scores every candidate against the requirements, "
                "and delivers a **ranked shortlist in minutes** — not days."
            )
            c1, c2, c3 = st.columns(3)
            c1.metric("Candidates in DB", f"{CRM_STATS['total_candidates']:,}")
            c2.metric("Active Jobs", CRM_STATS["active_jobs"])
            c3.metric("Shortlists Generated", CRM_STATS["shortlists_generated"])

        st.markdown("")

        # Engine 3
        with st.container(border=True):
            st.markdown("#### ⚙️ Engine 3: Manage Operations")
            st.markdown(
                "Processes call transcripts into structured data, analyzes email "
                "replies for sentiment, and keeps your CRM clean — automatically. "
                "Zero data entry required."
            )
            c1, c2, c3 = st.columns(3)
            c1.metric("Positive Reply Rate", CRM_STATS["positive_reply_rate"])
            c2.metric("Contacts", f"{CRM_STATS['total_contacts']:,}")
            c3.metric("Active Jobs", CRM_STATS["active_jobs"])

    with right:
        st.markdown("### Live Activity Feed")
        st.markdown("*All actions are automated — no human intervention*")
        st.markdown("")

        activities = generate_activity_log()
        for act in activities:
            time_ago = _time_ago(act["time"])
            st.markdown(
                f"{act['icon']} **{time_ago}** — {act['message']}"
            )
            st.markdown("", unsafe_allow_html=True)


def _time_ago(dt):
    """Format a datetime as a human-readable 'time ago' string."""
    from datetime import datetime
    diff = datetime.now() - dt
    seconds = diff.total_seconds()
    if seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    elif seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    else:
        return f"{int(seconds // 86400)}d ago"


# ---------------------------------------------------------------------------
# Page: Lead Generation Pipeline
# ---------------------------------------------------------------------------

def page_lead_gen():
    st.markdown("## 🔥 Lead Generation Pipeline")
    st.markdown(
        "Watch the system process a new lead end-to-end. "
        "Every signal — website visit, LinkedIn engagement, job posting — "
        "goes through the **same 10-step pipeline** automatically."
    )
    st.markdown("---")

    # Company selector
    col1, col2 = st.columns([2, 1])
    with col1:
        company_names = [c["name"] for c in COMPANIES]
        selected = st.selectbox(
            "Choose a company to process",
            company_names,
            index=0,
        )
        company_idx = company_names.index(selected)
        company = COMPANIES[company_idx]
        signal = SIGNALS.get(company["domain"], {})

    with col2:
        st.markdown("")
        st.markdown("")
        signal_label = signal.get("source", "unknown").replace("_", " ").title()
        st.markdown(f"**Signal:** {signal_label}")
        st.markdown(f"**Domain:** `{company['domain']}`")

    st.markdown("---")

    # Run pipeline button
    if st.button("▶ Run Lead Pipeline", type="primary", use_container_width=True):
        st.markdown("### Pipeline Execution")
        render_pipeline(simulate_process_lead(company_idx))

        st.markdown("---")
        st.balloons()
        st.markdown("### ✅ Pipeline Complete")

        # Summary card
        q = QUALIFICATIONS.get(company["domain"], {})
        score = q.get("score", 0)
        if score >= 8 and signal.get("intent") == "high":
            priority = "HOT 🔥"
            color = "red"
        elif score >= 5:
            priority = "WARM 🟡"
            color = "orange"
        else:
            priority = "COLD 🔵"
            color = "blue"

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ICP Score", f"{score}/10")
        with col2:
            st.metric("Priority", priority)
        with col3:
            contacts = DECISION_MAKERS.get(company["domain"], [])
            st.metric("Decision Makers Found", len(contacts))

    else:
        # Show what will happen
        st.markdown("### Pipeline Steps Preview")
        steps = [
            "1. **Signal Detection** — Identify the source and context",
            "2. **CRM Deduplication** — Check if company already exists",
            "3. **Company Enrichment** — Pull company data from Apollo",
            "4. **Decision Maker Discovery** — Find the right people to contact",
            "5. **Email Verification** — Verify deliverability via BetterContact",
            "6. **ICP Qualification** — AI evaluates fit against your ideal customer",
            "7. **Lead Scoring** — Assign Hot / Warm / Cold priority",
            "8. **Save to CRM** — Store everything in AirTable",
            "9. **Route to Outreach** — Add to the right campaign (Lemlist or Instantly)",
            "10. **Team Notification** — Alert your team via Slack",
        ]
        for step in steps:
            st.markdown(step)


# ---------------------------------------------------------------------------
# Page: Candidate Matching
# ---------------------------------------------------------------------------

def page_candidate_matching():
    st.markdown("## 👥 Candidate Matching Engine")
    st.markdown(
        "Enter job requirements and watch the system search your CRM, "
        "source from external databases, score every candidate with AI, "
        "and deliver a **ranked shortlist in under 2 minutes**."
    )
    st.markdown("---")

    # Show the demo job
    job = DEMO_JOB
    with st.container(border=True):
        st.markdown(f"### 📋 {job['title']}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Company:** {job['company']}")
            st.markdown(f"**Skills:** {job['skills_required']}")
        with col2:
            st.markdown(f"**Seniority:** {job['seniority']}")
            st.markdown(f"**Location:** {job['location']}")
        with col3:
            st.markdown(f"**Salary:** {job['salary_range']}")
            st.markdown(f"**Urgency:** {job['urgency']}")

    st.markdown("---")

    if st.button("▶ Find & Score Candidates", type="primary", use_container_width=True):
        st.markdown("### Matching Pipeline")

        # Collect results from generator
        scored_candidates = None
        for step_num, step_name, status, detail in simulate_match_candidates():
            if status == "running":
                with st.status(f"Step {step_num}: {step_name}", expanded=True):
                    st.markdown(detail)
                    time.sleep(0.3)  # Brief display
            elif status == "done":
                st.success(f"**Step {step_num}: {step_name}** ✓\n\n{detail}")

        st.markdown("---")
        st.balloons()

        # Show the shortlist as a detailed table
        st.markdown("### 🏆 Final Shortlist")

        for i, c in enumerate(CANDIDATES, 1):
            s = CANDIDATE_SCORES.get(c["name"], {})
            score = s.get("score", 0)

            if score >= 8:
                badge = "🟢"
            elif score >= 6:
                badge = "🟡"
            else:
                badge = "🔴"

            with st.container(border=True):
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.markdown(f"### #{i}")
                    st.markdown(f"## {badge} {score}/10")
                with col2:
                    st.markdown(f"**{c['name']}** — {c['title']} at {c['company']}")
                    st.markdown(f"📍 {c['location']} · {c['experience_years']} years exp · Source: {c['source'].title()}")
                    st.markdown(f"**Skills:** {c['skills']}")
                    if s.get("summary"):
                        st.markdown(f"*{s['summary']}*")
                with col3:
                    if s.get("strengths"):
                        st.markdown("**Strengths:**")
                        for strength in s["strengths"][:2]:
                            st.markdown(f"✅ {strength}")
                    if s.get("gaps"):
                        st.markdown("**Gaps:**")
                        for gap in s["gaps"][:1]:
                            st.markdown(f"⚠️ {gap}")


# ---------------------------------------------------------------------------
# Page: Transcript Processing
# ---------------------------------------------------------------------------

def page_transcript():
    st.markdown("## 📞 Call Transcript Processing")
    st.markdown(
        "When a call ends, Fathom sends the transcript. The system automatically "
        "extracts structured data — job requirements, candidate skills, next steps — "
        "and saves everything to your CRM. **Zero typing required.**"
    )
    st.markdown("---")

    # Show transcript excerpt
    t = DEMO_TRANSCRIPT
    with st.expander("📝 View Transcript Excerpt", expanded=False):
        st.code(t["transcript_excerpt"], language=None)

    st.markdown("---")

    if st.button("▶ Process Transcript", type="primary", use_container_width=True):
        st.markdown("### Processing Pipeline")
        render_pipeline(simulate_process_transcript())

        st.markdown("---")
        st.balloons()

        # Show extracted data beautifully
        st.markdown("### 📋 Extracted Job Requirements")
        ex = t["extracted_data"]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Title:** {ex['title']}")
            st.markdown(f"**Skills:** {ex['skills_required']}")
            st.markdown(f"**Seniority:** {ex['seniority']}")
            st.markdown(f"**Location:** {ex['location']}")
        with col2:
            st.markdown(f"**Salary:** {ex['salary_range']}")
            st.markdown(f"**Urgency:** {ex['urgency']}")
            st.markdown(f"**Team Size:** {ex['team_size']}")

        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Must-Haves:**")
            for mh in ex["must_haves"]:
                st.markdown(f"- ✅ {mh}")
        with col2:
            st.markdown("**Nice-to-Haves:**")
            for nh in ex["nice_to_haves"]:
                st.markdown(f"- 💡 {nh}")

        st.markdown("")
        st.info(f"**Culture Notes:** {ex['culture_notes']}")

        st.markdown("")
        st.warning(
            "⚡ **What happens next:** Because urgency is HIGH, the system "
            "automatically triggers candidate matching. A shortlist of scored "
            "candidates will be ready within 2 minutes."
        )


# ---------------------------------------------------------------------------
# Page: Reply Handling
# ---------------------------------------------------------------------------

def page_reply():
    st.markdown("## 📧 Email Reply Handling")
    st.markdown(
        "When a lead replies to your outreach, the system analyzes sentiment "
        "using AI and takes instant action — **positive replies get a Slack alert "
        "within seconds**, so your team can call while the lead is still warm."
    )
    st.markdown("---")

    # Reply selector
    reply_options = [
        f"✅ Positive — {EMAIL_REPLIES[0]['from'].split('<')[0].strip()}",
        f"✅ Positive — {EMAIL_REPLIES[1]['from'].split('<')[0].strip()}",
        f"❌ Negative — Unsubscribe request",
    ]
    selected = st.selectbox("Choose a reply to process", reply_options)
    reply_idx = reply_options.index(selected)

    # Show the email
    reply = EMAIL_REPLIES[reply_idx]
    with st.container(border=True):
        st.markdown(f"**From:** {reply['from']}")
        st.markdown(f"**Subject:** {reply['subject']}")
        st.markdown("---")
        st.markdown(reply["body"])

    st.markdown("---")

    if st.button("▶ Analyze Reply", type="primary", use_container_width=True):
        st.markdown("### Analysis Pipeline")
        render_pipeline(simulate_reply_handling(reply_idx))

        if reply["sentiment"] == "positive":
            st.markdown("---")
            st.balloons()
            st.markdown(
                "### 🚀 Speed-to-Lead\n\n"
                "The system detected a **positive reply** and immediately:\n"
                "1. Analyzed the sentiment and intent\n"
                "2. Assigned a recruiter from the rotation\n"
                "3. Sent an **urgent Slack alert** to call within 5 minutes\n\n"
                "Average response time with RecruitingOS: **< 5 minutes** "
                "(vs. industry average of **24-48 hours**)"
            )


# ---------------------------------------------------------------------------
# Page: System Architecture
# ---------------------------------------------------------------------------

def page_architecture():
    st.markdown("## 📊 System Architecture")
    st.markdown(
        "The system is built on a **3-layer architecture** that separates "
        "intent from execution. This makes it reliable, testable, and extensible."
    )
    st.markdown("---")

    # Architecture overview
    st.markdown("""
### How It All Connects

```
SIGNAL SOURCES                    CORE ENGINE                      OUTPUTS
────────────────                  ────────────────                 ──────────────
                                  ┌──────────────┐
Job Postings (Google) ──────┐     │              │     ┌─── Lemlist (hot leads)
                            ├────▶│ process_lead │────▶├─── Instantly (warm leads)
Website Visitors (RB2B) ────┤     │   (10 steps) │     ├─── AirTable CRM
                            │     │              │     └─── Slack alerts
LinkedIn Engagement ────────┤     └──────────────┘
                            │
Lookalike Companies ────────┘     ┌──────────────┐
                                  │  process_    │     ┌─── Structured CRM data
Call Recordings ─────────────────▶│  transcript  │────▶├─── Follow-up tasks
                                  │  (6 steps)   │     └─── Auto-trigger matching
                                  └──────────────┘
                                  ┌──────────────┐
New Job Openings ────────────────▶│    match_    │────▶──── Ranked shortlist
                                  │  candidates  │         (scored 1-10)
                                  │  (8 steps)   │
                                  └──────────────┘
```
    """)

    st.markdown("---")

    # Tech stack
    st.markdown("### Technology Stack — 15 Integrated Tools")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Data & Enrichment")
        st.markdown("- **Apollo** — Company + people data")
        st.markdown("- **Apify** — Google Jobs scraping")
        st.markdown("- **BetterContact** — Email verification")
        st.markdown("- **RB2B / Vector** — Website visitor ID")
        st.markdown("- **Taplio** — LinkedIn engagement tracking")

    with col2:
        st.markdown("#### Intelligence & CRM")
        st.markdown("- **OpenAI GPT-4o** — Qualification, scoring, extraction")
        st.markdown("- **AirTable** — CRM (5 tables)")
        st.markdown("- **Fathom** — Call recording & transcripts")

    with col3:
        st.markdown("#### Outreach & Ops")
        st.markdown("- **Lemlist** — Multi-channel outreach (hot)")
        st.markdown("- **Instantly** — Email sequences (warm)")
        st.markdown("- **Slack** — Real-time team notifications")
        st.markdown("- **Modal** — Cloud hosting (webhooks + crons)")

    st.markdown("---")

    # What runs automatically
    st.markdown("### What Runs Automatically")

    auto_items = [
        {"time": "Every day at 6:00 AM", "action": "Scrape Google Jobs → Enrich → Qualify → Route leads", "engine": "Lead Gen"},
        {"time": "Every Monday at 7:00 AM", "action": "CRM health check: re-enrich stale data, archive inactive, flag missing emails", "engine": "Operations"},
        {"time": "Instantly (webhook)", "action": "Website visitor identified → Full lead pipeline in < 60 seconds", "engine": "Lead Gen"},
        {"time": "Instantly (webhook)", "action": "LinkedIn engagement detected → Classify + route automatically", "engine": "Lead Gen"},
        {"time": "Instantly (webhook)", "action": "Email reply received → Sentiment analyzed → Recruiter alerted in < 5 min", "engine": "Operations"},
        {"time": "Instantly (webhook)", "action": "Call ends → Transcript extracted → Job record created → Matching triggered", "engine": "Candidate"},
        {"time": "Instantly (webhook)", "action": "New job added → Candidates searched + scored → Shortlist in 2 min", "engine": "Candidate"},
    ]

    df = pd.DataFrame(auto_items)
    df.columns = ["When", "What Happens", "Engine"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Cost breakdown
    st.markdown("### Monthly Operating Cost")
    st.markdown("*Based on processing ~200 leads/month*")

    cost_data = [
        {"Tool": "OpenAI (GPT-4o)", "Cost": "$20-50", "Notes": "Qualification + scoring + extraction"},
        {"Tool": "Apollo", "Cost": "$50-100", "Notes": "Company enrichment + people search"},
        {"Tool": "Apify", "Cost": "$10-30", "Notes": "Google Jobs scraping"},
        {"Tool": "BetterContact", "Cost": "$20-50", "Notes": "Email verification (only when needed)"},
        {"Tool": "Modal (hosting)", "Cost": "$0-10", "Notes": "Free tier covers most usage"},
        {"Tool": "AirTable", "Cost": "$0-20", "Notes": "Free tier may be sufficient"},
        {"Tool": "TOTAL", "Cost": "$100-260", "Notes": "Replaces 15+ hours/week of manual work"},
    ]

    df_cost = pd.DataFrame(cost_data)
    st.dataframe(df_cost, use_container_width=True, hide_index=True)

    st.markdown("")
    st.info(
        "**ROI Comparison:** One junior recruiter doing this manually costs $3,000-5,000/month. "
        "This system does the same work for $100-260/month — and it runs 24/7 without breaks."
    )


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

if "🏠" in page:
    page_dashboard()
elif "🔥" in page:
    page_lead_gen()
elif "👥" in page:
    page_candidate_matching()
elif "📞" in page:
    page_transcript()
elif "📧" in page:
    page_reply()
elif "📊" in page:
    page_architecture()
