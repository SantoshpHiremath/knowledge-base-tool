"""End-to-end pipeline: build the corpus, evaluate search quality, run
governance checks, simulate a query log and detect gaps, compute metrics,
and print a combined KM report.
"""
from datetime import date

from corpus import build_corpus, TODAY
from search import KnowledgeBaseSearch
from governance import governance_report
from gap_detection import log_queries, gap_summary
from metrics import search_success_rate, most_and_least_viewed

# Evaluation queries with known-correct expected articles (real relevance
# evaluation, not just "it returns something").
EVAL_QUERIES = [
    ("how do I reset my password", "How to Reset Your Password"),
    ("phishing awareness", "Phishing Awareness Guide"),
    ("booking a conference room", "Booking a Meeting Room"),
    ("how much vacation do I have", "Vacation Request Process"),
    ("my laptop was stolen what do I do", "Reporting a Lost or Stolen Device"),
    ("setting up two factor authentication", "Setting Up Two-Factor Authentication"),
    ("sprint planning process", "Sprint Planning Guidelines"),
    ("parental leave how does it work", "Parental Leave Policy"),
]

# Simulated real-world query log: a mix of well-covered topics (repeated,
# as real users would ask the same thing many ways) and genuine gaps
# (topics the corpus has no article for).
SIMULATED_QUERY_LOG = (
    ["how do I reset my password"] * 12
    + ["vpn access request"] * 8
    + ["vacation days remaining"] * 6
    + ["report phishing email"] * 5
    + ["how do I set up direct deposit for my paycheck"] * 7
    + ["what is the dress code policy"] * 4
    + ["how do I request a company credit card"] * 3
    + ["where do I find the org chart"] * 5
    + ["sprint planning guidelines"] * 4
)

SIMULATED_ACCESS_LOG = (
    ["How to Reset Your Password"] * 40
    + ["How to Request VPN Access"] * 25
    + ["Vacation Request Process"] * 20
    + ["Phishing Awareness Guide"] * 15
    + ["Sprint Planning Guidelines"] * 10
    + ["Onboarding: Setting Up Your Laptop"] * 8
)


def run():
    articles = build_corpus()
    kb = KnowledgeBaseSearch(articles)

    print(f"Knowledge base: {len(articles)} synthetic articles.\n")

    print("=== Search Quality Evaluation ===")
    correct = 0
    for query, expected_title in EVAL_QUERIES:
        article, score = kb.best_match(query)
        ok = article.title == expected_title
        correct += ok
        print(f"  {'OK  ' if ok else 'MISS'} {query!r} -> {article.title!r} (score={score:.3f})")
    print(f"  {correct}/{len(EVAL_QUERIES)} correct on known-answer evaluation queries\n")

    print("=== Content Governance Report ===")
    gov = governance_report(articles, TODAY)
    print(f"  Stale articles: {gov['stale_count']}/{gov['total_articles']} ({gov['stale_pct']}%)")
    for title in gov["stale_articles"]:
        print(f"    - {title}")
    print(f"  Incomplete articles: {gov['incomplete_count']}/{gov['total_articles']} ({gov['incomplete_pct']}%)")
    for entry in gov["incomplete_articles"]:
        print(f"    - {entry['title']}: {', '.join(entry['issues'])}")

    print("\n=== Knowledge Gap Detection (simulated query log) ===")
    records = log_queries(kb, SIMULATED_QUERY_LOG)
    summary = gap_summary(records)
    print(f"  {summary['gap_hit_count']}/{summary['total_queries']} queries ({summary['gap_hit_pct']}%) hit a knowledge gap")
    print("  Top unanswered topics:")
    for gap in summary["top_gaps"]:
        print(f"    - {gap['query']!r} (asked {gap['count']}x)")

    print("\n=== KM Effectiveness Metrics ===")
    rate = search_success_rate(records)
    print(f"  Search success rate: {rate * 100:.1f}%")
    views = most_and_least_viewed(SIMULATED_ACCESS_LOG, articles)
    print("  Most viewed:", views["most_viewed"])
    print("  Least viewed (candidates for review or removal):", views["least_viewed"])


if __name__ == "__main__":
    run()
