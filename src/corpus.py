"""A SYNTHETIC knowledge-base corpus — not real E.ON documentation.
Modeled on a typical internal wiki: onboarding guides, tool how-tos, HR
policy pages, project-process docs, and security guidance. Some articles
are deliberately stale (old last_updated) or missing metadata (no owner/
tags/category), mirroring a real, imperfectly-maintained wiki rather than
a pristine synthetic one — so the governance checks have real issues to
find.
"""
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Article:
    article_id: int
    title: str
    body: str
    category: str | None
    tags: list
    owner: str | None
    last_updated: str  # ISO date string


TODAY = date(2026, 8, 7)

_RAW_ARTICLES = [
    # (title, body, category, tags, owner, last_updated)
    ("Onboarding: Setting Up Your Laptop", "Steps to configure your company laptop on your first day, including VPN setup, email configuration, and required software installs.", "onboarding", ["onboarding", "IT", "laptop"], "IT-Support", "2026-06-01"),
    ("Onboarding: First Week Checklist", "A checklist for new hires covering badge access, benefits enrollment, meeting your buddy, and completing mandatory training.", "onboarding", ["onboarding", "checklist"], "HR-Ops", "2026-05-15"),
    ("Onboarding: Meeting Your Team", "Guidance on scheduling introductory meetings with your team and manager during your first two weeks.", "onboarding", ["onboarding", "team"], "HR-Ops", "2023-02-10"),  # stale
    ("How to Request VPN Access", "Instructions for requesting VPN access for remote work, including required approvals and setup steps.", "it_tools", ["VPN", "remote work", "IT"], "IT-Support", "2026-07-01"),
    ("How to Reset Your Password", "Self-service password reset instructions and what to do if you're locked out of your account.", "it_tools", ["password", "account", "IT"], "IT-Support", "2026-06-20"),
    ("Using the Internal Wiki", "Guide to navigating, searching, and contributing to the internal knowledge base.", "it_tools", ["wiki", "documentation"], None, "2026-01-05"),  # missing owner
    ("Booking a Meeting Room", "How to check room availability and book a conference room through the calendar system.", "it_tools", [], "Facilities", "2026-04-11"),  # missing tags
    ("Setting Up Two-Factor Authentication", "Steps to enroll a device for two-factor authentication on your company account.", "it_tools", ["security", "2FA", "IT"], "IT-Support", "2026-07-20"),
    ("Vacation Request Process", "How to submit and track vacation requests through the HR portal, including approval timelines.", "hr_policy", ["vacation", "HR", "leave"], "HR-Ops", "2026-03-01"),
    ("Expense Reimbursement Guide", "Step-by-step process for submitting expense reports and expected reimbursement timelines.", "hr_policy", ["expenses", "reimbursement", "HR"], "HR-Ops", "2026-02-18"),
    ("Parental Leave Policy", "Overview of parental leave entitlements, application process, and return-to-work support.", "hr_policy", ["parental leave", "HR", "policy"], "HR-Ops", "2022-11-01"),  # stale
    ("Remote Work Policy", "Company guidelines on remote and hybrid work arrangements, including eligibility and expectations.", "hr_policy", ["remote work", "policy", "HR"], "HR-Ops", "2026-05-30"),
    ("Health Insurance Enrollment", "Information on enrolling in or updating your health insurance plan and key deadlines.", "hr_policy", ["insurance", "benefits", "HR"], None, "2026-06-10"),  # missing owner
    ("Sabbatical Request Guidance", "Process and eligibility criteria for requesting an extended sabbatical leave.", "hr_policy", ["sabbatical", "HR"], "HR-Ops", "2021-09-01"),  # stale
    ("Project Kickoff Checklist", "Standard checklist for kicking off a new project, including stakeholder alignment and charter creation.", "project_process", ["project management", "kickoff"], "PMO", "2026-04-22"),
    ("Sprint Planning Guidelines", "How our teams run sprint planning sessions, including estimation practices and backlog grooming.", "project_process", ["agile", "sprint planning"], "PMO", "2026-06-15"),
    ("Change Request Process", "Steps for submitting, reviewing, and approving a change request for an in-flight project.", "project_process", ["change management", "process"], "PMO", "2026-01-30"),
    ("Post-Project Retrospective Template", "A template and guide for running an effective retrospective after project completion.", "project_process", ["retrospective", "agile"], None, "2024-08-01"),  # stale + missing owner
    ("Stakeholder Communication Plan Template", "Template for creating a stakeholder communication plan at project start.", None, ["stakeholders", "communication"], "PMO", "2026-05-01"),  # missing category
    ("Security Incident Reporting", "How to report a suspected security incident and what happens after you report it.", "security", ["security", "incident", "reporting"], "Security-Team", "2026-07-10"),
    ("Phishing Awareness Guide", "How to recognize and report phishing attempts, with recent examples from our environment.", "security", ["phishing", "security", "awareness"], "Security-Team", "2026-06-25"),
    ("Data Classification Policy", "How to classify and handle company data according to sensitivity level.", "security", ["data", "classification", "policy"], "Security-Team", "2022-03-15"),  # stale
    ("Acceptable Use Policy", "Guidelines on acceptable use of company devices, networks, and accounts.", "security", ["policy", "acceptable use"], "Security-Team", "2026-02-01"),
    ("Reporting a Lost or Stolen Device", "Steps to take immediately if your company laptop or phone is lost or stolen.", "security", ["security", "device", "IT"], "IT-Support", "2026-07-28"),
    ("Setting Up Multi-Factor Authentication Apps", "Comparison and setup guide for supported authenticator apps.", "it_tools", ["MFA", "security", "IT"], "IT-Support", "2026-07-05"),
    ("Requesting Software Licenses", "Process for requesting a new software license or renewing an existing one.", "it_tools", ["software", "licenses", "IT"], "IT-Support", "2026-03-18"),
    ("New Hire Equipment Request", "How managers request laptops and peripherals for incoming new hires.", "onboarding", ["onboarding", "equipment"], "IT-Support", "2026-05-20"),
    ("Internal Mentorship Program Overview", "How the mentorship program works and how to sign up as a mentor or mentee.", "hr_policy", ["mentorship", "development"], "HR-Ops", "2026-04-01"),
    ("Travel Booking Guidelines", "How to book business travel through the approved travel portal and expense it correctly.", "project_process", ["travel", "expenses"], "PMO", "2020-06-01"),  # stale
    ("Wiki Contribution Standards", "Formatting, tagging, and review standards for contributing new articles to the knowledge base.", "it_tools", ["wiki", "standards", "documentation"], "KM-Team", "2026-07-15"),
]


def build_corpus():
    articles = []
    for i, (title, body, category, tags, owner, last_updated) in enumerate(_RAW_ARTICLES):
        articles.append(Article(
            article_id=i + 1,
            title=title,
            body=body,
            category=category,
            tags=tags,
            owner=owner,
            last_updated=last_updated,
        ))
    return articles


if __name__ == "__main__":
    articles = build_corpus()
    print(f"Corpus: {len(articles)} synthetic articles.")
    from collections import Counter
    print("By category:", Counter(a.category for a in articles))
