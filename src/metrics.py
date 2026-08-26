"""KM effectiveness metrics — models "monitor and analyze knowledge
management metrics to measure the effectiveness of knowledge sharing
initiatives" from the posting.
"""
from collections import defaultdict


def search_success_rate(query_records, threshold=0.30):
    """Fraction of queries that got a 'good enough' answer (score >=
    threshold) — the headline KM-effectiveness number."""
    if not query_records:
        return None
    hits = sum(1 for r in query_records if r["score"] >= threshold)
    return round(hits / len(query_records), 4)


def article_view_counts(access_log):
    """access_log: list of article titles representing simulated page
    views. Returns {title: count}."""
    counts = defaultdict(int)
    for title in access_log:
        counts[title] += 1
    return dict(counts)


def most_and_least_viewed(access_log, articles, top_n=3):
    counts = article_view_counts(access_log)
    all_titles = [a.title for a in articles]
    # Articles never viewed still count as 0 — a real "least viewed"
    # report needs to surface completely-ignored content, not just the
    # lowest nonzero count.
    full_counts = {title: counts.get(title, 0) for title in all_titles}
    ranked = sorted(full_counts.items(), key=lambda kv: kv[1], reverse=True)
    return {
        "most_viewed": ranked[:top_n],
        "least_viewed": ranked[-top_n:][::-1],
    }
