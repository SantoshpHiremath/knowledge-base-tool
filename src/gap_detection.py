"""Simulates a stream of user search queries and detects which ones the
knowledge base consistently fails to answer well — the "identify knowledge gaps"
step of knowledge management.
"""
from collections import defaultdict

DEFAULT_GAP_THRESHOLD = 0.30


def log_queries(search_engine, queries):
    """queries: list of query strings (may repeat — a real query log has
    the same underlying question asked many different ways/times).
    Returns a list of {"query": str, "best_title": str|None, "score": float} records.
    """
    records = []
    for q in queries:
        article, score = search_engine.best_match(q)
        records.append({
            "query": q,
            "best_title": article.title if article else None,
            "score": float(score),
        })
    return records


def detect_gaps(query_records, threshold=DEFAULT_GAP_THRESHOLD):
    """A query is a 'gap hit' if its best-match score is below threshold
    — the knowledge base doesn't have a good answer for it. Groups gap
    hits and returns them ranked by frequency, since a knowledge gap that
    comes up repeatedly is a stronger signal than a one-off unanswered
    query."""
    gap_hits = [r for r in query_records if r["score"] < threshold]

    counts = defaultdict(int)
    for hit in gap_hits:
        counts[hit["query"]] += 1

    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return [{"query": q, "count": c} for q, c in ranked]


def gap_summary(query_records, threshold=DEFAULT_GAP_THRESHOLD):
    total = len(query_records)
    gap_hits = [r for r in query_records if r["score"] < threshold]
    return {
        "total_queries": total,
        "gap_hit_count": len(gap_hits),
        "gap_hit_pct": round(len(gap_hits) / total * 100, 1) if total else 0.0,
        "top_gaps": detect_gaps(query_records, threshold)[:5],
    }
