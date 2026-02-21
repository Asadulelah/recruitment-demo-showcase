"""
Mock data for the RecruitingOS demo.
All data is realistic but completely fictional.
"""

import random
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Companies (leads that come through the pipeline)
# ---------------------------------------------------------------------------

COMPANIES = [
    {
        "domain": "talentbridge.io",
        "name": "TalentBridge Staffing",
        "industry": "Staffing and Recruiting",
        "headcount": 34,
        "funding": "Series A — $4.2M",
        "linkedin_url": "linkedin.com/company/talentbridge",
        "location": "Austin, TX",
        "tech_stack": ["Bullhorn", "LinkedIn Recruiter", "HubSpot"],
        "description": "Boutique tech staffing firm specializing in cloud engineering and DevOps placements across the US.",
    },
    {
        "domain": "apexhire.com",
        "name": "Apex Hire Partners",
        "industry": "Staffing and Recruiting",
        "headcount": 22,
        "funding": "Bootstrapped — $3.1M revenue",
        "linkedin_url": "linkedin.com/company/apexhire",
        "location": "London, UK",
        "tech_stack": ["Vincere", "LinkedIn Recruiter"],
        "description": "Executive search firm focused on fintech and banking leadership roles in the UK and EU.",
    },
    {
        "domain": "meridiantalent.co",
        "name": "Meridian Talent Group",
        "industry": "Staffing and Recruiting",
        "headcount": 45,
        "funding": "Private — $6.8M revenue",
        "linkedin_url": "linkedin.com/company/meridiantalent",
        "location": "Chicago, IL",
        "tech_stack": ["Bullhorn", "Loxo", "Gem"],
        "description": "Full-cycle recruitment agency covering healthcare, engineering, and IT verticals.",
    },
    {
        "domain": "novarecruit.com",
        "name": "Nova Recruit",
        "industry": "Staffing and Recruiting",
        "headcount": 18,
        "funding": "Bootstrapped — $2.4M revenue",
        "linkedin_url": "linkedin.com/company/novarecruit",
        "location": "Toronto, Canada",
        "tech_stack": ["Mercury xRM", "LinkedIn Recruiter"],
        "description": "Tech staffing agency specializing in AI/ML and data engineering placements.",
    },
    {
        "domain": "eliteplacements.co.uk",
        "name": "Elite Placements Ltd",
        "industry": "Staffing and Recruiting",
        "headcount": 28,
        "funding": "Bootstrapped — $4.7M revenue",
        "linkedin_url": "linkedin.com/company/eliteplacements",
        "location": "Manchester, UK",
        "tech_stack": ["Bullhorn", "Sourcebreaker"],
        "description": "Retained search firm for C-suite and VP-level hires in tech and manufacturing.",
    },
    {
        "domain": "catalystpeople.com",
        "name": "Catalyst People Solutions",
        "industry": "Staffing and Recruiting",
        "headcount": 15,
        "funding": "Seed — $1.2M",
        "linkedin_url": "linkedin.com/company/catalystpeople",
        "location": "Sydney, Australia",
        "tech_stack": ["Loxo", "HubSpot"],
        "description": "Startup-focused recruitment agency placing product and engineering talent across APAC.",
    },
]

# ---------------------------------------------------------------------------
# Decision makers (contacts at the companies above)
# ---------------------------------------------------------------------------

DECISION_MAKERS = {
    "talentbridge.io": [
        {"name": "Sarah Mitchell", "title": "CEO & Founder", "email": "sarah@talentbridge.io", "linkedin": "linkedin.com/in/sarahmitchell"},
        {"name": "James Ortega", "title": "VP of Operations", "email": "james@talentbridge.io", "linkedin": "linkedin.com/in/jamesortega"},
    ],
    "apexhire.com": [
        {"name": "David Chen", "title": "Managing Director", "email": "david@apexhire.com", "linkedin": "linkedin.com/in/davidchen"},
        {"name": "Emily Watson", "title": "Head of Business Development", "email": "emily@apexhire.com", "linkedin": "linkedin.com/in/emilywatson"},
    ],
    "meridiantalent.co": [
        {"name": "Rachel Foster", "title": "CEO", "email": "rachel@meridiantalent.co", "linkedin": "linkedin.com/in/rachelfoster"},
        {"name": "Mark Simmons", "title": "Director of Recruiting", "email": "mark@meridiantalent.co", "linkedin": "linkedin.com/in/marksimmons"},
    ],
    "novarecruit.com": [
        {"name": "Alex Petrov", "title": "Founder & CEO", "email": "alex@novarecruit.com", "linkedin": "linkedin.com/in/alexpetrov"},
    ],
    "eliteplacements.co.uk": [
        {"name": "Catherine Hughes", "title": "Managing Partner", "email": "catherine@eliteplacements.co.uk", "linkedin": "linkedin.com/in/catherinehughes"},
        {"name": "Tom Blackwell", "title": "Principal Consultant", "email": "tom@eliteplacements.co.uk", "linkedin": "linkedin.com/in/tomblackwell"},
    ],
    "catalystpeople.com": [
        {"name": "Ryan Patel", "title": "CEO", "email": "ryan@catalystpeople.com", "linkedin": "linkedin.com/in/ryanpatel"},
    ],
}

# ---------------------------------------------------------------------------
# Signal sources (how the lead was discovered)
# ---------------------------------------------------------------------------

SIGNALS = {
    "talentbridge.io": {
        "source": "website_visitor",
        "detail": "Visited /pricing and /case-studies pages",
        "pages_visited": ["/pricing", "/case-studies", "/how-it-works"],
        "intent": "high",
    },
    "apexhire.com": {
        "source": "linkedin",
        "detail": "Liked and commented on your LinkedIn post about AI in recruitment",
        "engagement_type": "comment",
        "intent": "high",
    },
    "meridiantalent.co": {
        "source": "job_scraping",
        "detail": "Posted 3 new job listings for 'Data Engineer' roles",
        "jobs_posted": ["Senior Data Engineer", "Lead Data Engineer", "Data Engineering Manager"],
        "intent": "medium",
    },
    "novarecruit.com": {
        "source": "job_scraping",
        "detail": "Posted job for 'Head of Recruitment Operations'",
        "jobs_posted": ["Head of Recruitment Operations"],
        "intent": "high",
    },
    "eliteplacements.co.uk": {
        "source": "lookalike",
        "detail": "Similar to closed client (same size, same vertical, same tech stack)",
        "intent": "medium",
    },
    "catalystpeople.com": {
        "source": "linkedin",
        "detail": "CEO followed your company page and liked 2 posts",
        "engagement_type": "follow + like",
        "intent": "medium",
    },
}

# ---------------------------------------------------------------------------
# ICP qualification results (what OpenAI would say)
# ---------------------------------------------------------------------------

QUALIFICATIONS = {
    "talentbridge.io": {
        "icp_fit": True,
        "score": 9,
        "reasoning": "Perfect ICP fit. 34 employees in staffing & recruiting. Uses Bullhorn (proves tech maturity and budget). Based in US. Visited pricing page — strong buying intent. Series A funded with growth mandate.",
        "priority_factors": ["Visited pricing page", "Tech staffing niche (high fees)", "Bullhorn user (has budget)"],
    },
    "apexhire.com": {
        "icp_fit": True,
        "score": 8,
        "reasoning": "Strong fit. 22 employees, fintech search firm in London. Engaged with AI recruitment content on LinkedIn — indicates active interest in automation. Revenue suggests healthy budget.",
        "priority_factors": ["LinkedIn engagement", "Executive search (high ACV)", "UK market"],
    },
    "meridiantalent.co": {
        "icp_fit": True,
        "score": 7,
        "reasoning": "Good fit. 45 employees across 3 verticals. Large enough to benefit from automation. Currently posting jobs suggesting active growth phase. Uses Bullhorn + Loxo (tech savvy).",
        "priority_factors": ["Multi-vertical (large TAM)", "Active hiring signals", "Multiple ATS tools"],
    },
    "novarecruit.com": {
        "icp_fit": True,
        "score": 9,
        "reasoning": "Excellent fit. Hiring for 'Head of Recruitment Operations' signals operational pain. AI/ML staffing niche means high placement fees. Tech-forward audience will understand the value immediately.",
        "priority_factors": ["Hiring for ops role (clear pain)", "AI/ML niche (premium fees)", "CEO is sole decision maker"],
    },
    "eliteplacements.co.uk": {
        "icp_fit": True,
        "score": 6,
        "reasoning": "Moderate fit. Retained search firm with good revenue. Similar profile to existing client. However, UK market and retained model may mean longer sales cycle. Worth pursuing as warm lead.",
        "priority_factors": ["Similar to existing client", "Retained search (high fees)", "Bullhorn user"],
    },
    "catalystpeople.com": {
        "icp_fit": True,
        "score": 7,
        "reasoning": "Good fit. Startup-focused agency in APAC. CEO showed interest via LinkedIn. Smaller team (15) but Seed funding suggests growth ambitions. Product + engineering placements are high-value.",
        "priority_factors": ["CEO interest", "Growth stage", "High-value placements"],
    },
}

# ---------------------------------------------------------------------------
# Candidates (for the matching demo)
# ---------------------------------------------------------------------------

CANDIDATES = [
    {
        "name": "Priya Sharma",
        "email": "priya.sharma@gmail.com",
        "title": "Senior Software Engineer",
        "company": "Stripe",
        "skills": "Python, Go, AWS, Kubernetes, Microservices, PostgreSQL",
        "experience_years": 7,
        "location": "San Francisco, CA",
        "linkedin": "linkedin.com/in/priyasharma",
        "source": "internal",
    },
    {
        "name": "Marcus Johnson",
        "email": "marcus.j@outlook.com",
        "title": "Lead Backend Engineer",
        "company": "Shopify",
        "skills": "Python, Ruby, AWS, Docker, Redis, GraphQL",
        "experience_years": 9,
        "location": "Toronto, Canada",
        "linkedin": "linkedin.com/in/marcusjohnson",
        "source": "internal",
    },
    {
        "name": "Elena Popova",
        "email": "elena.p@protonmail.com",
        "title": "Staff Engineer",
        "company": "Datadog",
        "skills": "Python, Go, Kubernetes, Terraform, CI/CD, Monitoring",
        "experience_years": 11,
        "location": "New York, NY",
        "linkedin": "linkedin.com/in/elenapopova",
        "source": "internal",
    },
    {
        "name": "Daniel Kim",
        "email": "daniel.kim@gmail.com",
        "title": "Senior DevOps Engineer",
        "company": "Twilio",
        "skills": "Python, Terraform, AWS, GCP, Docker, Kubernetes, Jenkins",
        "experience_years": 6,
        "location": "Seattle, WA",
        "linkedin": "linkedin.com/in/danielkim",
        "source": "apollo",
    },
    {
        "name": "Aisha Okafor",
        "email": "aisha.o@yahoo.com",
        "title": "Platform Engineer",
        "company": "Cloudflare",
        "skills": "Go, Python, Rust, Kubernetes, Linux, Networking",
        "experience_years": 8,
        "location": "Austin, TX",
        "linkedin": "linkedin.com/in/aishaokafor",
        "source": "apollo",
    },
    {
        "name": "Thomas Weber",
        "email": "t.weber@gmail.com",
        "title": "Senior Software Engineer",
        "company": "Zalando",
        "skills": "Java, Python, AWS, Kafka, Microservices, Spring Boot",
        "experience_years": 10,
        "location": "Berlin, Germany",
        "linkedin": "linkedin.com/in/thomasweber",
        "source": "apollo",
    },
    {
        "name": "Sophie Chen",
        "email": "sophie.chen@gmail.com",
        "title": "Engineering Manager",
        "company": "Meta",
        "skills": "Python, C++, System Design, Team Leadership, ML Infra",
        "experience_years": 12,
        "location": "Menlo Park, CA",
        "linkedin": "linkedin.com/in/sophiechen",
        "source": "apollo",
    },
    {
        "name": "Omar Hassan",
        "email": "omar.h@gmail.com",
        "title": "Cloud Infrastructure Engineer",
        "company": "MongoDB",
        "skills": "Python, Go, AWS, Terraform, MongoDB, Docker",
        "experience_years": 5,
        "location": "Dublin, Ireland",
        "linkedin": "linkedin.com/in/omarhassan",
        "source": "apollo",
    },
]

CANDIDATE_SCORES = {
    "Priya Sharma": {"score": 9, "strengths": ["Strong Python + cloud stack", "Kubernetes expert", "7 years at top-tier company"], "gaps": ["No management experience"], "summary": "Exceptional technical match. Stripe pedigree adds credibility. Would be a strong IC contributor immediately."},
    "Marcus Johnson": {"score": 8, "strengths": ["Lead-level experience", "Python + cloud", "9 years experience"], "gaps": ["Ruby background (not required)", "Canada-based (relocation?)"], "summary": "Strong lead candidate with relevant stack. Experience at Shopify demonstrates scale expertise."},
    "Elena Popova": {"score": 9, "strengths": ["Staff-level engineer", "11 years experience", "Full DevOps + platform skill set"], "gaps": ["May be overqualified for senior role", "Salary expectations likely high"], "summary": "Top-tier candidate. Staff engineer at Datadog with deep infrastructure expertise. Flight risk if role isn't senior enough."},
    "Daniel Kim": {"score": 7, "strengths": ["Strong DevOps background", "Multi-cloud experience"], "gaps": ["6 years may be junior for role", "No team lead experience"], "summary": "Solid mid-senior candidate. Good technical breadth but may need another 1-2 years for lead roles."},
    "Aisha Okafor": {"score": 8, "strengths": ["Platform engineering at scale", "Rust + Go (rare combo)", "Cloudflare pedigree"], "gaps": ["Less Python-focused", "May prefer platform over application work"], "summary": "Strong platform engineer with rare skill combination. Cloudflare background means real scale experience."},
    "Thomas Weber": {"score": 6, "strengths": ["10 years experience", "Microservices expertise"], "gaps": ["Java-primary (Python secondary)", "EU timezone", "Visa/relocation needed for US roles"], "summary": "Experienced but Java-focused. Good for EU-based roles. Python is secondary skill."},
    "Sophie Chen": {"score": 7, "strengths": ["Engineering management at Meta", "12 years total experience", "ML infrastructure background"], "gaps": ["Management track (not hands-on IC)", "Meta comp = high salary expectations"], "summary": "Strong if role needs leadership. Overqualified for pure IC roles. Salary expectations will be $300K+."},
    "Omar Hassan": {"score": 6, "strengths": ["Cloud infra skills", "MongoDB + Python", "Dublin-based (EU coverage)"], "gaps": ["Only 5 years experience", "No Kubernetes experience listed"], "summary": "Junior-mid level. Good for growing teams that can invest in development. Not ready for senior roles."},
}

# ---------------------------------------------------------------------------
# Job openings (for matching demo)
# ---------------------------------------------------------------------------

DEMO_JOB = {
    "title": "Senior Cloud Infrastructure Engineer",
    "company": "TechVentures Inc.",
    "skills_required": "Python, AWS, Kubernetes, Terraform, Docker",
    "seniority": "Senior",
    "location": "Remote (US preferred)",
    "salary_range": "$180,000 — $220,000",
    "urgency": "High — backfill for departing team lead",
    "must_haves": ["Python", "AWS", "Kubernetes"],
    "nice_to_haves": ["Terraform", "Go", "CI/CD pipeline experience"],
}

# ---------------------------------------------------------------------------
# Email replies (for reply handling demo)
# ---------------------------------------------------------------------------

EMAIL_REPLIES = [
    {
        "from": "Sarah Mitchell <sarah@talentbridge.io>",
        "subject": "Re: AI-Powered Recruitment Infrastructure",
        "body": "Hi there,\n\nThis is really interesting. We've been struggling with exactly these problems — our recruiters spend half their day on data entry instead of actually recruiting.\n\nI'd love to learn more about how this works in practice. Could we set up a 30-minute call this week?\n\nBest,\nSarah",
        "sentiment": "positive",
        "is_interested": True,
        "reasoning": "Clear buying signals: acknowledges pain point, asks for call, time-sensitive language.",
        "suggested_action": "Book call within 24 hours. Send calendar link immediately.",
    },
    {
        "from": "David Chen <david@apexhire.com>",
        "subject": "Re: Streamline Your Search Operations",
        "body": "Thanks for reaching out. We're actually in the middle of evaluating a few automation tools.\n\nCan you send over some case studies or results from agencies similar to ours (exec search, 20-30 people)?\n\nDavid",
        "sentiment": "positive",
        "is_interested": True,
        "reasoning": "Evaluating solutions = active buyer. Requesting case studies = due diligence phase. Size-specific question shows serious interest.",
        "suggested_action": "Send tailored case study within 2 hours. Follow up with call booking.",
    },
    {
        "from": "info@randomcorp.com",
        "subject": "Re: Partnership Opportunity",
        "body": "Please remove me from your mailing list.\n\nThanks",
        "sentiment": "negative",
        "is_interested": False,
        "reasoning": "Explicit unsubscribe request. No engagement with content.",
        "suggested_action": "Remove from all campaigns. Mark as 'Not Interested'. Do not re-contact.",
    },
]

# ---------------------------------------------------------------------------
# Transcript excerpt (for transcript processing demo)
# ---------------------------------------------------------------------------

DEMO_TRANSCRIPT = {
    "meeting_title": "Client Briefing — TechVentures hiring",
    "meeting_id": "fathom_meeting_12345",
    "duration": "28 minutes",
    "transcript_excerpt": """
[00:00] Recruiter: Thanks for joining, Mark. Let's talk about this role you need filled.

[00:15] Client (Mark, VP Engineering at TechVentures): Sure. So we lost our lead cloud infrastructure engineer last month. He was basically running our entire AWS setup — Kubernetes clusters, Terraform configs, the CI/CD pipeline. We need someone senior who can own all of that.

[02:30] Recruiter: Got it. What's the tech stack specifically?

[02:45] Client: Primary is Python for tooling and automation. AWS is non-negotiable — we're all-in on AWS. Kubernetes for orchestration, Terraform for infrastructure as code. Docker obviously. If they know Go that's a bonus but not required.

[04:10] Recruiter: Seniority level?

[04:20] Client: Senior. At least 6-7 years experience. Someone who's owned infrastructure at a company our size — we're about 200 engineers. Not a FAANG person who only knows one microservice. We need a generalist who can own the whole stack.

[06:00] Recruiter: Location?

[06:10] Client: Remote is fine but US timezone preferred. We have stand-ups at 10am ET.

[08:30] Recruiter: Budget?

[08:45] Client: $180K to $220K base. We can flex on equity.

[10:00] Recruiter: Timeline?

[10:15] Client: Yesterday. Seriously though, our current setup is running but nobody's maintaining it properly. I'd love shortlisted candidates within a week.

[12:00] Recruiter: Understood. Any must-haves vs. nice-to-haves?

[12:20] Client: Must-haves: Python, AWS, Kubernetes. Nice-to-haves: Terraform experience, Go, any CI/CD pipeline work. The biggest thing is ownership mentality — someone who treats the infrastructure like it's their own product.
""",
    "extracted_data": {
        "title": "Senior Cloud Infrastructure Engineer",
        "skills_required": "Python, AWS, Kubernetes, Terraform, Docker",
        "seniority": "Senior (6-7+ years)",
        "location": "Remote (US timezone preferred)",
        "salary_range": "$180,000 — $220,000 + equity",
        "urgency": "High — backfill, needs shortlist within 1 week",
        "team_size": "200 engineers",
        "must_haves": ["Python", "AWS", "Kubernetes"],
        "nice_to_haves": ["Terraform", "Go", "CI/CD pipeline experience"],
        "culture_notes": "Wants ownership mentality. Not interested in FAANG specialists — needs generalists.",
    },
}

# ---------------------------------------------------------------------------
# CRM summary stats (for dashboard)
# ---------------------------------------------------------------------------

CRM_STATS = {
    "total_companies": 847,
    "total_contacts": 1_423,
    "total_candidates": 2_156,
    "active_jobs": 12,
    "leads_this_week": 43,
    "hot_leads": 8,
    "warm_leads": 22,
    "cold_leads": 13,
    "meetings_booked": 5,
    "emails_sent": 312,
    "reply_rate": "14.2%",
    "positive_reply_rate": "8.7%",
    "shortlists_generated": 7,
    "placements_this_month": 3,
}

# ---------------------------------------------------------------------------
# Activity log (recent events)
# ---------------------------------------------------------------------------

def generate_activity_log():
    """Generate a realistic activity log for the last 7 days."""
    now = datetime.now()
    activities = [
        {"time": now - timedelta(minutes=12), "type": "lead", "message": "TalentBridge Staffing — HOT lead (9/10) → Added to Lemlist campaign", "icon": "🔥"},
        {"time": now - timedelta(minutes=45), "type": "lead", "message": "Apex Hire Partners — HOT lead (8/10) via LinkedIn engagement → Added to Lemlist", "icon": "🔥"},
        {"time": now - timedelta(hours=2), "type": "reply", "message": "Sarah Mitchell (TalentBridge) replied POSITIVELY — Meeting requested!", "icon": "📧"},
        {"time": now - timedelta(hours=3), "type": "lead", "message": "Meridian Talent Group — WARM lead (7/10) via job scraping → Added to Instantly", "icon": "🟡"},
        {"time": now - timedelta(hours=5), "type": "candidate", "message": "Shortlist ready: Senior Cloud Infrastructure Engineer — 8 candidates scored", "icon": "👥"},
        {"time": now - timedelta(hours=8), "type": "transcript", "message": "Client briefing processed: TechVentures — Job record created automatically", "icon": "📞"},
        {"time": now - timedelta(hours=12), "type": "lead", "message": "Nova Recruit — HOT lead (9/10) via job scraping → Added to Lemlist", "icon": "🔥"},
        {"time": now - timedelta(days=1), "type": "lead", "message": "Elite Placements — WARM lead (6/10) via lookalike discovery → Added to Instantly", "icon": "🟡"},
        {"time": now - timedelta(days=1, hours=3), "type": "lead", "message": "Catalyst People Solutions — WARM lead (7/10) via LinkedIn → Added to Instantly", "icon": "🟡"},
        {"time": now - timedelta(days=1, hours=6), "type": "reply", "message": "David Chen (Apex Hire) replied — Requesting case studies", "icon": "📧"},
        {"time": now - timedelta(days=2), "type": "cron", "message": "Daily job scraping complete: 47 jobs → 12 new companies → 4 qualified leads", "icon": "⚙️"},
        {"time": now - timedelta(days=2, hours=4), "type": "candidate", "message": "Candidate screening processed: Priya Sharma — High engagement, strong fit", "icon": "👤"},
        {"time": now - timedelta(days=3), "type": "cron", "message": "Daily job scraping complete: 52 jobs → 15 new companies → 6 qualified leads", "icon": "⚙️"},
        {"time": now - timedelta(days=4), "type": "crm", "message": "Weekly CRM health: 12 records re-enriched, 3 archived, 2 emails flagged", "icon": "🔧"},
    ]
    return activities
