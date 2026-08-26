"""Test suite for the knowledge-base search, governance, and gap-detection tool."""
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from corpus import build_corpus, Article, TODAY
from search import KnowledgeBaseSearch
from governance import is_stale, completeness_issues, is_complete, governance_report
from gap_detection import log_queries, detect_gaps, gap_summary
from metrics import search_success_rate, article_view_counts, most_and_least_viewed


@pytest.fixture
def articles():
    return build_corpus()


@pytest.fixture
def kb(articles):
    return KnowledgeBaseSearch(articles)


# --- Corpus ------------------------------------------------------------------

def test_corpus_has_expected_size(articles):
    assert len(articles) == 30


def test_every_article_has_unique_id(articles):
    ids = [a.article_id for a in articles]
    assert len(ids) == len(set(ids))


# --- Search: relevance evaluated against known-correct answers --------------

@pytest.mark.parametrize("query,expected_title", [
    ("how do I reset my password", "How to Reset Your Password"),
    ("phishing awareness", "Phishing Awareness Guide"),
    ("booking a conference room", "Booking a Meeting Room"),
    ("how much vacation do I have", "Vacation Request Process"),
    ("my laptop was stolen what do I do", "Reporting a Lost or Stolen Device"),
    ("setting up two factor authentication", "Setting Up Two-Factor Authentication"),
    ("sprint planning process", "Sprint Planning Guidelines"),
    ("parental leave how does it work", "Parental Leave Policy"),
])
def test_search_returns_correct_top_result(kb, query, expected_title):
    article, score = kb.best_match(query)
    assert article.title == expected_title


def test_search_score_for_relevant_query_is_reasonably_high(kb):
    _, score = kb.best_match("how do I reset my password")
    assert score > 0.5


def test_search_score_for_irrelevant_query_is_low(kb):
    _, score = kb.best_match("how do I set up direct deposit for my paycheck")
    assert score < 0.30


def test_search_returns_top_k_results_in_descending_score_order(kb):
    results = kb.search("password reset account locked", top_k=5)
    scores = [score for _, score in results]
    assert scores == sorted(scores, reverse=True)
    assert len(results) <= 5


def test_best_match_matches_first_search_result(kb):
    top_result = kb.search("VPN access", top_k=1)[0]
    best = kb.best_match("VPN access")
    assert top_result[0].title == best[0].title
    assert top_result[1] == best[1]


# --- Governance: staleness --------------------------------------------------

def test_is_stale_true_for_old_article():
    article = Article(1, "Old Doc", "body", "cat", ["tag"], "owner", "2020-01-01")
    assert is_stale(article, TODAY) is True


def test_is_stale_false_for_recent_article():
    article = Article(1, "New Doc", "body", "cat", ["tag"], "owner", "2026-07-01")
    assert is_stale(article, TODAY) is False


def test_is_stale_respects_custom_threshold():
    article = Article(1, "Doc", "body", "cat", ["tag"], "owner", "2026-06-01")
    # ~67 days old as of TODAY (2026-08-07) — stale at a 30-day threshold,
    # not stale at a 365-day threshold.
    assert is_stale(article, TODAY, stale_days=30) is True
    assert is_stale(article, TODAY, stale_days=365) is False


def test_governance_report_stale_count_matches_corpus(articles):
    report = governance_report(articles, TODAY)
    manual_stale = [a for a in articles if is_stale(a, TODAY)]
    assert report["stale_count"] == len(manual_stale)
    assert set(report["stale_articles"]) == {a.title for a in manual_stale}


# --- Governance: completeness ------------------------------------------------

def test_completeness_issues_detects_missing_owner():
    article = Article(1, "Doc", "body", "cat", ["tag"], None, "2026-01-01")
    assert "missing_owner" in completeness_issues(article)


def test_completeness_issues_detects_missing_tags():
    article = Article(1, "Doc", "body", "cat", [], "owner", "2026-01-01")
    assert "missing_tags" in completeness_issues(article)


def test_completeness_issues_detects_missing_category():
    article = Article(1, "Doc", "body", None, ["tag"], "owner", "2026-01-01")
    assert "missing_category" in completeness_issues(article)


def test_is_complete_true_when_no_issues():
    article = Article(1, "Doc", "body", "cat", ["tag"], "owner", "2026-01-01")
    assert is_complete(article) is True
    assert completeness_issues(article) == []


def test_governance_report_incomplete_count_matches_corpus(articles):
    report = governance_report(articles, TODAY)
    manual_incomplete = [a for a in articles if not is_complete(a)]
    assert report["incomplete_count"] == len(manual_incomplete)


# --- Gap detection -----------------------------------------------------------

def test_log_queries_produces_one_record_per_query(kb):
    queries = ["password reset", "vacation days", "unknown topic xyz"]
    records = log_queries(kb, queries)
    assert len(records) == 3
    assert all("query" in r and "score" in r and "best_title" in r for r in records)


def test_detect_gaps_flags_low_score_queries_only():
    records = [
        {"query": "well answered", "best_title": "X", "score": 0.8},
        {"query": "poorly answered", "best_title": "Y", "score": 0.1},
    ]
    gaps = detect_gaps(records, threshold=0.3)
    gap_queries = {g["query"] for g in gaps}
    assert "poorly answered" in gap_queries
    assert "well answered" not in gap_queries


def test_detect_gaps_counts_repeated_queries():
    records = [{"query": "repeated gap", "best_title": None, "score": 0.05} for _ in range(4)]
    records.append({"query": "one-off gap", "best_title": None, "score": 0.05})
    gaps = detect_gaps(records, threshold=0.3)
    top = gaps[0]
    assert top["query"] == "repeated gap"
    assert top["count"] == 4


def test_gap_summary_percentages_are_consistent():
    records = [{"query": f"q{i}", "best_title": None, "score": 0.1 if i < 3 else 0.9} for i in range(10)]
    summary = gap_summary(records, threshold=0.3)
    assert summary["total_queries"] == 10
    assert summary["gap_hit_count"] == 3
    assert summary["gap_hit_pct"] == 30.0


def test_real_gap_queries_are_detected_end_to_end(kb):
    """Integration check: genuinely gap-y queries against the real corpus
    should surface as gaps, not just in a synthetic unit test."""
    log = ["how do I set up direct deposit for my paycheck"] * 3 + ["how do I reset my password"] * 3
    records = log_queries(kb, log)
    gaps = detect_gaps(records)
    gap_queries = {g["query"] for g in gaps}
    assert "how do I set up direct deposit for my paycheck" in gap_queries
    assert "how do I reset my password" not in gap_queries


# --- Metrics -------------------------------------------------------------

def test_search_success_rate_matches_manual_calculation():
    records = [{"score": s} for s in [0.8, 0.9, 0.1, 0.5, 0.05]]
    rate = search_success_rate(records, threshold=0.3)
    manual = sum(1 for r in records if r["score"] >= 0.3) / len(records)
    assert rate == round(manual, 4)


def test_search_success_rate_none_for_empty_log():
    assert search_success_rate([]) is None


def test_article_view_counts_matches_manual_tally():
    log = ["A", "A", "B", "C", "A"]
    counts = article_view_counts(log)
    assert counts == {"A": 3, "B": 1, "C": 1}


def test_most_and_least_viewed_includes_zero_view_articles(articles):
    # Only view 2 of the 30 articles — the rest should still appear in
    # "least viewed" with a count of 0, not be silently dropped.
    log = [articles[0].title] * 5 + [articles[1].title] * 2
    result = most_and_least_viewed(log, articles, top_n=3)
    least_titles = [title for title, count in result["least_viewed"]]
    least_counts = [count for title, count in result["least_viewed"]]
    assert all(c == 0 for c in least_counts)
    assert result["most_viewed"][0] == (articles[0].title, 5)
