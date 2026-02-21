"""
Demo engine — simulated core functions that show each pipeline step.
Uses mock data instead of real API calls. Yields step-by-step status
updates for the Streamlit UI to render in real time.
"""

import time
from mock_data import (
    COMPANIES, DECISION_MAKERS, SIGNALS, QUALIFICATIONS,
    CANDIDATES, CANDIDATE_SCORES, DEMO_JOB, DEMO_TRANSCRIPT,
    EMAIL_REPLIES,
)


def simulate_process_lead(company_index=0):
    """
    Generator that yields (step_number, step_name, status, detail) tuples.
    Simulates process_lead() with realistic delays.
    """
    company = COMPANIES[company_index]
    domain = company["domain"]
    contacts = DECISION_MAKERS.get(domain, [])
    signal = SIGNALS.get(domain, {})
    qualification = QUALIFICATIONS.get(domain, {})

    # Step 1: Signal detected
    yield (1, "Signal Detected", "running",
           f"Source: **{signal.get('source', 'unknown').replace('_', ' ').title()}**\n\n"
           f"{signal.get('detail', '')}")
    time.sleep(0.8)
    yield (1, "Signal Detected", "done",
           f"Source: **{signal.get('source', 'unknown').replace('_', ' ').title()}**\n\n"
           f"{signal.get('detail', '')}")

    # Step 2: Deduplication check
    yield (2, "CRM Deduplication", "running",
           f"Checking AirTable for existing record: `{domain}`")
    time.sleep(0.6)
    yield (2, "CRM Deduplication", "done",
           f"No existing record found for `{domain}` — proceeding with enrichment")

    # Step 3: Company enrichment
    yield (3, "Company Enrichment (Apollo)", "running",
           f"Querying Apollo API for `{domain}`...")
    time.sleep(1.2)
    enrichment_detail = (
        f"**{company['name']}**\n\n"
        f"| Field | Value |\n"
        f"|-------|-------|\n"
        f"| Industry | {company['industry']} |\n"
        f"| Headcount | {company['headcount']} employees |\n"
        f"| Funding | {company['funding']} |\n"
        f"| Location | {company['location']} |\n"
        f"| Tech Stack | {', '.join(company['tech_stack'])} |\n"
        f"| Description | {company['description']} |"
    )
    yield (3, "Company Enrichment (Apollo)", "done", enrichment_detail)

    # Step 4: Decision maker discovery
    yield (4, "Find Decision Makers (Apollo)", "running",
           f"Searching for decision makers at {company['name']}...")
    time.sleep(1.0)
    contact_lines = ""
    for c in contacts:
        contact_lines += f"- **{c['name']}** — {c['title']} ({c['email']})\n"
    if not contact_lines:
        contact_lines = "No decision makers found"
    yield (4, "Find Decision Makers (Apollo)", "done",
           f"Found **{len(contacts)} decision maker(s)**:\n\n{contact_lines}")

    # Step 5: Email verification
    primary = contacts[0] if contacts else None
    if primary and primary.get("email"):
        yield (5, "Email Verification (BetterContact)", "running",
               f"Verifying {primary['email']}...")
        time.sleep(0.7)
        yield (5, "Email Verification (BetterContact)", "done",
               f"Verified: **{primary['email']}** is deliverable")
    else:
        yield (5, "Email Verification (BetterContact)", "running",
               "Searching for email address...")
        time.sleep(1.5)
        yield (5, "Email Verification (BetterContact)", "done",
               "Email found via waterfall lookup")

    # Step 6: AI Qualification
    yield (6, "ICP Qualification (OpenAI GPT-4o)", "running",
           "Analyzing company against Ideal Customer Profile...")
    time.sleep(1.5)
    q = qualification
    qual_detail = (
        f"**Score: {q['score']}/10** — {'Qualified' if q['icp_fit'] else 'Not Qualified'}\n\n"
        f"**Reasoning:** {q['reasoning']}\n\n"
        f"**Key Factors:**\n"
    )
    for factor in q.get("priority_factors", []):
        qual_detail += f"- {factor}\n"
    yield (6, "ICP Qualification (OpenAI GPT-4o)", "done", qual_detail)

    # Step 7: Lead scoring
    score = q["score"]
    high_intent = signal.get("intent") == "high"
    if score >= 8 and high_intent:
        priority = "HOT"
        priority_emoji = "🔥"
    elif score >= 5:
        priority = "WARM"
        priority_emoji = "🟡"
    else:
        priority = "COLD"
        priority_emoji = "🔵"

    yield (7, "Lead Scoring", "running", "Calculating priority...")
    time.sleep(0.5)
    yield (7, "Lead Scoring", "done",
           f"**{priority_emoji} {priority}** — Score: {score}/10, "
           f"Intent: {'High' if high_intent else 'Medium'}")

    # Step 8: Save to CRM
    yield (8, "Save to CRM (AirTable)", "running",
           "Creating company and contact records...")
    time.sleep(0.8)
    yield (8, "Save to CRM (AirTable)", "done",
           f"Saved: **{company['name']}** + {len(contacts)} contact(s) to AirTable")

    # Step 9: Route to outreach
    if priority == "HOT":
        campaign_tool = "Lemlist (multi-channel: email + LinkedIn)"
    elif priority == "WARM":
        campaign_tool = "Instantly (email sequence)"
    else:
        campaign_tool = "No outreach — CRM only"

    yield (9, "Route to Outreach", "running",
           f"Adding to {campaign_tool}...")
    time.sleep(0.8)
    if primary:
        yield (9, "Route to Outreach", "done",
               f"**{primary['name']}** ({primary['email']}) added to **{campaign_tool}**")
    else:
        yield (9, "Route to Outreach", "done",
               f"Routed to: **{campaign_tool}**")

    # Step 10: Slack notification
    yield (10, "Team Notification (Slack)", "running", "Sending alert...")
    time.sleep(0.4)
    yield (10, "Team Notification (Slack)", "done",
           f"{priority_emoji} **New {priority} Lead:** {company['name']} "
           f"({score}/10) via {signal.get('source', 'unknown').replace('_', ' ')}")


def simulate_match_candidates():
    """
    Generator that yields (step_number, step_name, status, detail) tuples.
    Simulates match_candidates() for the demo job.
    """
    job = DEMO_JOB

    yield (1, "Job Requirements", "running", "Loading job requirements...")
    time.sleep(0.5)
    job_detail = (
        f"**{job['title']}** at {job['company']}\n\n"
        f"| Field | Value |\n"
        f"|-------|-------|\n"
        f"| Skills | {job['skills_required']} |\n"
        f"| Seniority | {job['seniority']} |\n"
        f"| Location | {job['location']} |\n"
        f"| Salary | {job['salary_range']} |\n"
        f"| Urgency | {job['urgency']} |"
    )
    yield (1, "Job Requirements", "done", job_detail)

    # Step 2: Internal CRM search
    internal = [c for c in CANDIDATES if c["source"] == "internal"]
    yield (2, "Search Internal CRM (AirTable)", "running",
           f"Searching for candidates matching: Python, AWS, Kubernetes...")
    time.sleep(1.0)
    internal_lines = ""
    for c in internal:
        internal_lines += f"- **{c['name']}** — {c['title']} at {c['company']} ({c['experience_years']}y exp)\n"
    yield (2, "Search Internal CRM (AirTable)", "done",
           f"Found **{len(internal)} internal candidates**:\n\n{internal_lines}")

    # Step 3: External search
    external = [c for c in CANDIDATES if c["source"] == "apollo"]
    yield (3, "Search External (Apollo)", "running",
           f"Only {len(internal)} internal matches (need 10+). Searching Apollo...")
    time.sleep(1.5)
    external_lines = ""
    for c in external:
        external_lines += f"- **{c['name']}** — {c['title']} at {c['company']} ({c['experience_years']}y exp)\n"
    yield (3, "Search External (Apollo)", "done",
           f"Found **{len(external)} external candidates** on Apollo:\n\n{external_lines}")

    # Step 4: Merge + dedupe
    yield (4, "Merge & Deduplicate", "running",
           f"Merging {len(internal)} internal + {len(external)} external...")
    time.sleep(0.5)
    yield (4, "Merge & Deduplicate", "done",
           f"**{len(CANDIDATES)} unique candidates** after deduplication")

    # Step 5: AI scoring
    yield (5, "AI Scoring (OpenAI GPT-4o)", "running",
           f"Batch scoring {len(CANDIDATES)} candidates against job requirements...\n\n"
           f"*Evaluating: skills match, seniority fit, location compatibility, career trajectory*")
    time.sleep(2.0)

    scored = []
    for c in CANDIDATES:
        s = CANDIDATE_SCORES.get(c["name"], {})
        scored.append({**c, **s})
    scored.sort(key=lambda x: x.get("score", 0), reverse=True)

    score_lines = ""
    for i, c in enumerate(scored[:5], 1):
        stars = "★" * c.get("score", 0) + "☆" * (10 - c.get("score", 0))
        score_lines += f"{i}. **{c['name']}** — {c.get('score', 0)}/10 {stars}\n"
    yield (5, "AI Scoring (OpenAI GPT-4o)", "done",
           f"All candidates scored. **Top 5:**\n\n{score_lines}")

    # Step 6: Build shortlist
    shortlist = scored[:5]
    yield (6, "Build Shortlist", "running", "Generating shortlist with summaries...")
    time.sleep(0.8)
    yield (6, "Build Shortlist", "done",
           f"**Shortlist of {len(shortlist)} candidates ready** — see results below")

    # Step 7: Save to CRM
    yield (7, "Save to CRM (AirTable)", "running",
           "Linking candidates to job record...")
    time.sleep(0.6)
    yield (7, "Save to CRM (AirTable)", "done",
           f"Job status updated to **'Shortlisted'**. {len(shortlist)} candidates linked.")

    # Step 8: Notify team
    yield (8, "Team Notification (Slack)", "running", "Sending shortlist alert...")
    time.sleep(0.4)
    yield (8, "Team Notification (Slack)", "done",
           f"👥 **Shortlist Ready:** {job['title']} — {len(shortlist)} candidates scored and ranked")

    return scored


def simulate_process_transcript():
    """
    Generator that yields (step_number, step_name, status, detail) tuples.
    Simulates process_transcript() for a client briefing.
    """
    t = DEMO_TRANSCRIPT

    yield (1, "Transcript Received (Fathom)", "running",
           f"Meeting: *{t['meeting_title']}*\nDuration: {t['duration']}")
    time.sleep(0.5)
    yield (1, "Transcript Received (Fathom)", "done",
           f"Meeting: *{t['meeting_title']}*\nDuration: {t['duration']}\n\n"
           f"Full transcript retrieved ({len(t['transcript_excerpt'])} characters)")

    # Step 2: Classify call type
    yield (2, "Classify Call Type", "running",
           "Analyzing meeting title for keywords...")
    time.sleep(0.6)
    yield (2, "Classify Call Type", "done",
           "Title contains **'Client Briefing'** → Type: **Client Briefing**\n\n"
           "*(Keywords detected: 'briefing', 'client')*")

    # Step 3: AI extraction
    yield (3, "Extract Structured Data (OpenAI GPT-4o)", "running",
           "Sending transcript to GPT-4o for structured extraction...\n\n"
           "*Extracting: job title, skills, seniority, location, salary, urgency, must-haves*")
    time.sleep(2.0)

    ex = t["extracted_data"]
    extracted_detail = (
        f"**Extracted Job Requirements:**\n\n"
        f"| Field | Extracted Value |\n"
        f"|-------|----------------|\n"
        f"| Title | {ex['title']} |\n"
        f"| Skills | {ex['skills_required']} |\n"
        f"| Seniority | {ex['seniority']} |\n"
        f"| Location | {ex['location']} |\n"
        f"| Salary | {ex['salary_range']} |\n"
        f"| Urgency | {ex['urgency']} |\n"
        f"| Team Size | {ex['team_size']} |\n\n"
        f"**Must-Haves:** {', '.join(ex['must_haves'])}\n\n"
        f"**Nice-to-Haves:** {', '.join(ex['nice_to_haves'])}\n\n"
        f"**Culture Notes:** {ex['culture_notes']}"
    )
    yield (3, "Extract Structured Data (OpenAI GPT-4o)", "done", extracted_detail)

    # Step 4: Create job record
    yield (4, "Create Job Record (AirTable)", "running",
           "Saving extracted requirements to CRM...")
    time.sleep(0.8)
    yield (4, "Create Job Record (AirTable)", "done",
           f"Job record created: **{ex['title']}**\nStatus: **New**")

    # Step 5: Trigger candidate matching
    yield (5, "Auto-Trigger Candidate Matching", "running",
           "Urgency is HIGH — automatically triggering candidate search...")
    time.sleep(0.6)
    yield (5, "Auto-Trigger Candidate Matching", "done",
           "Candidate matching triggered. Shortlist will be ready in ~2 minutes.")

    # Step 6: Notify team
    yield (6, "Team Notification (Slack)", "running", "Sending alert...")
    time.sleep(0.4)
    yield (6, "Team Notification (Slack)", "done",
           f"📞 **Client Briefing Processed:** {ex['title']}\n"
           f"Urgency: {ex['urgency']}\n"
           f"Candidate matching auto-triggered")


def simulate_reply_handling(reply_index=0):
    """
    Generator that yields (step_number, step_name, status, detail) tuples.
    Simulates reply_handler for an email reply.
    """
    reply = EMAIL_REPLIES[reply_index]

    yield (1, "Email Reply Received (Lemlist)", "running",
           f"**From:** {reply['from']}\n**Subject:** {reply['subject']}")
    time.sleep(0.5)
    yield (1, "Email Reply Received (Lemlist)", "done",
           f"**From:** {reply['from']}\n**Subject:** {reply['subject']}\n\n"
           f"---\n\n{reply['body']}")

    # Step 2: Sentiment analysis
    yield (2, "Sentiment Analysis (OpenAI GPT-4o)", "running",
           "Analyzing reply sentiment and intent...")
    time.sleep(1.2)

    sentiment_emoji = {"positive": "✅", "negative": "❌", "neutral": "➖"}
    emoji = sentiment_emoji.get(reply["sentiment"], "➖")

    yield (2, "Sentiment Analysis (OpenAI GPT-4o)", "done",
           f"**Sentiment:** {emoji} {reply['sentiment'].upper()}\n\n"
           f"**Interested:** {'Yes' if reply['is_interested'] else 'No'}\n\n"
           f"**Reasoning:** {reply['reasoning']}")

    # Step 3: Route action
    yield (3, "Route Action", "running", "Determining next steps...")
    time.sleep(0.6)

    if reply["sentiment"] == "positive":
        yield (3, "Route Action", "done",
               f"**Action:** {reply['suggested_action']}\n\n"
               f"**Assigned to:** Recruiter on rotation\n\n"
               f"**Priority:** URGENT — respond within 5 minutes")

        # Step 4: Urgent notification
        yield (4, "URGENT Slack Alert", "running", "Sending speed-to-lead alert...")
        time.sleep(0.5)
        yield (4, "URGENT Slack Alert", "done",
               f"🚨 **POSITIVE REPLY — CALL WITHIN 5 MINUTES**\n\n"
               f"**{reply['from'].split('<')[0].strip()}** responded to outreach.\n"
               f"Suggested action: {reply['suggested_action']}")
    elif reply["sentiment"] == "negative":
        yield (3, "Route Action", "done",
               f"**Action:** {reply['suggested_action']}\n\n"
               f"Lead removed from campaign. Status → 'Not Interested'")

        yield (4, "Update CRM", "running", "Marking as not interested...")
        time.sleep(0.5)
        yield (4, "Update CRM", "done",
               "Contact status updated to **'Not Interested'**. Removed from all campaigns.")
    else:
        yield (3, "Route Action", "done",
               "Neutral reply — logged but no urgent action needed.\n\n"
               "Will be reviewed in next weekly pipeline review.")
        yield (4, "Log Activity", "running", "Logging to activity log...")
        time.sleep(0.4)
        yield (4, "Log Activity", "done", "Activity logged. No follow-up required.")
