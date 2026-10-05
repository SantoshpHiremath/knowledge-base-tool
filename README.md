# Knowledge Base Search, Governance & Gap-Detection Tool

A tested Python tool that combines search and retrieval over a document
repository with content-governance checks and knowledge-gap detection.
It covers the core jobs of knowledge management: organizing a content
repository, checking content for accuracy and completeness, monitoring
KM metrics, and identifying where the knowledge base fails to answer
real questions.

## Scope

**This is not SharePoint, and the corpus is synthetic.** SharePoint is a
licensed Microsoft 365 cloud service and I don't have a tenant to build
against, so I built a local Python tool over a small synthetic "wiki" of
articles (onboarding guides, tool how-tos, policy pages — generated
content, not real company documentation).

**The search/retrieval is classical IR (TF-IDF + cosine similarity), not
an LLM.** I built it without LLM API access, so the "AI-enabled" search
piece is real search ranking evaluated against known-relevant results.

## What this models

- **`src/corpus.py`** — a synthetic knowledge base of ~30 articles across
  5 categories (onboarding, IT tools, HR policy, project processes,
  security), each with title, body text, tags, owner, category, and a
  `last_updated` date — some deliberately stale, some deliberately
  missing metadata, mirroring a real, imperfectly-maintained wiki rather
  than a pristine one.
- **`src/search.py`** — TF-IDF + cosine-similarity search over the
  corpus, returning ranked results with a relevance score, evaluated
  (not just built) against a set of test queries with known-correct
  expected articles.
- **`src/governance.py`** — content-governance checks: flags articles
  as **stale** (not updated within a configurable threshold) and as
  **incomplete** (missing owner, tags, or category), to check existing
  documentation for accuracy, completeness, and alignment with
  standards.
- **`src/gap_detection.py`** — simulates a stream of user search
  queries (some the corpus answers well, some it doesn't), logs each
  query's best-match relevance score, and aggregates the queries that
  consistently return poor matches into a ranked **knowledge-gap
  report**.
- **`src/metrics.py`** — KM effectiveness metrics: search success rate
  (fraction of queries with a good match), stale/incomplete article
  counts and percentages, and most-viewed/least-viewed articles from a
  simulated access log.
- **`src/pipeline.py`** — runs the full flow end-to-end and prints a
  combined KM report.

## Testing

25 automated tests (`tests/test_knowledge_base.py`) covering: search
relevance (8 known-answer queries, each checked against the specific
correct article, not just "it returns something"), staleness and
completeness detection against hand-checked expected results, gap
detection correctly separating well-answered from poorly-answered queries
(including an end-to-end check against the real corpus, not just
synthetic unit-test data), and metrics computed correctly against manual
recalculation.

## Running it

```bash
pip install scikit-learn
python3 src/pipeline.py          # builds the corpus, runs search evaluation, governance checks, gap detection, and metrics
python3 -m pytest tests/ -v      # runs all 25 tests
```
