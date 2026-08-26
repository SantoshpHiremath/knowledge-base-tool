# Knowledge Base Search, Governance & Gap-Detection Tool

A real, tested Python tool combining search/retrieval over a document
repository with content-governance checks and knowledge-gap detection —
built to close a specific gap for E.ON's "Working Student Knowledge
Management" posting, whose tasks (organizing repositories, checking
content accuracy/completeness, monitoring KM metrics, identifying
knowledge gaps, and supporting "AI-enabled knowledge management tools")
weren't covered by anything in my existing project portfolio.

## What this is (read before citing anywhere)

**This is not SharePoint, and the corpus is synthetic.** SharePoint is a
licensed Microsoft 365 cloud service — there's no tenant available to me
to build or test against, so rather than claim SharePoint experience I
don't have, I built the closest thing I could actually construct and
verify: a local Python tool over a small synthetic "wiki" of articles
(onboarding guides, tool how-tos, policy pages — generated content, not
real E.ON documentation).

**The search/retrieval is classical IR (TF-IDF + cosine similarity), not
an LLM.** I have no Claude/Gemini/OpenAI API access in this environment.
The posting's "AI-enabled knowledge management tools" task is addressed
honestly at the level I could actually build and test: real search
ranking, evaluated against known-relevant results, not a large language
model.

If asked in an interview: I haven't used SharePoint, and this isn't an
LLM-based system. This project demonstrates the underlying skills the
posting actually asks for — organizing a content repository, checking it
for staleness/completeness, measuring how well it serves real search
queries, and surfacing where it's failing to answer questions — built and
verified against a system I could construct myself.

## What this models

- **`src/corpus.py`** — a synthetic knowledge base of ~30 articles across
  5 categories (onboarding, IT tools, HR policy, project processes,
  security), each with title, body text, tags, owner, category, and a
  `last_updated` date — some deliberately stale, some deliberately
  missing metadata, mirroring a real, imperfectly-maintained wiki rather
  than a pristine one.
- **`src/search.py`** — TF-IDF + cosine-similarity search over the
  corpus, returning ranked results with a relevance score — the
  "AI-enabled" search piece, evaluated (not just built) against a set of
  test queries with known-correct expected articles.
- **`src/governance.py`** — content-governance checks: flags articles
  as **stale** (not updated within a configurable threshold) and as
  **incomplete** (missing owner, tags, or category) — the "analyze
  existing documentation for accuracy, completeness, and alignment with
  company standards" task.
- **`src/gap_detection.py`** — simulates a stream of real user search
  queries (some the corpus answers well, some it doesn't), logs each
  query's best-match relevance score, and aggregates the queries that
  consistently return poor matches into a ranked **knowledge-gap
  report** — directly modeling "collaborate to identify knowledge gaps."
- **`src/metrics.py`** — KM effectiveness metrics: search success rate
  (fraction of queries with a good match), stale/incomplete article
  counts and percentages, and most-viewed/least-viewed articles from a
  simulated access log — the "monitor and analyze knowledge management
  metrics" task.
- **`src/pipeline.py`** — runs the full flow end-to-end and prints a
  combined KM report.

## Verification

32 automated tests (`tests/test_knowledge_base.py`) covering: search
relevance (8 known-answer queries, each checked against the specific
correct article, not just "it returns something"), staleness and
completeness detection against hand-checked expected results, gap-
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
