"""Content-governance checks: staleness and metadata completeness.
Checks existing documentation for accuracy, completeness, and alignment
with standards, so information stays accurate, up-to-date, and easily accessible.
"""
from datetime import date

DEFAULT_STALE_DAYS = 365


def _parse_date(iso_str):
    y, m, d = (int(x) for x in iso_str.split("-"))
    return date(y, m, d)


def is_stale(article, today, stale_days=DEFAULT_STALE_DAYS):
    age_days = (today - _parse_date(article.last_updated)).days
    return age_days > stale_days


def completeness_issues(article):
    """Returns a list of missing-metadata issue strings for an article
    (empty list means fully complete)."""
    issues = []
    if not article.owner:
        issues.append("missing_owner")
    if not article.tags:
        issues.append("missing_tags")
    if not article.category:
        issues.append("missing_category")
    return issues


def is_complete(article):
    return len(completeness_issues(article)) == 0


def governance_report(articles, today, stale_days=DEFAULT_STALE_DAYS):
    stale = [a for a in articles if is_stale(a, today, stale_days)]
    incomplete = [a for a in articles if not is_complete(a)]

    return {
        "total_articles": len(articles),
        "stale_count": len(stale),
        "stale_articles": [a.title for a in stale],
        "incomplete_count": len(incomplete),
        "incomplete_articles": [
            {"title": a.title, "issues": completeness_issues(a)} for a in incomplete
        ],
        "stale_pct": round(len(stale) / len(articles) * 100, 1) if articles else 0.0,
        "incomplete_pct": round(len(incomplete) / len(articles) * 100, 1) if articles else 0.0,
    }
