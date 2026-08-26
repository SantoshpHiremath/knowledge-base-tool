"""TF-IDF + cosine-similarity search over the article corpus — the
"AI-enabled" search/retrieval piece. This is classical information
retrieval, not an LLM (no API access available). Evaluated against known-
correct results, not just "it returns something." See README.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class KnowledgeBaseSearch:
    def __init__(self, articles):
        self.articles = articles
        self.vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2), stop_words="english")
        corpus_texts = [self._article_text(a) for a in articles]
        self._matrix = self.vectorizer.fit_transform(corpus_texts)

    def _article_text(self, article):
        tag_text = " ".join(article.tags)
        return f"{article.title} {article.title} {article.body} {tag_text}"  # title weighted 2x

    def search(self, query, top_k=5):
        """Returns up to top_k (article, score) pairs sorted by
        descending relevance score (cosine similarity, 0-1)."""
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self._matrix)[0]
        ranked = sorted(zip(self.articles, scores), key=lambda pair: pair[1], reverse=True)
        return ranked[:top_k]

    def best_match(self, query):
        results = self.search(query, top_k=1)
        return results[0] if results else (None, 0.0)
