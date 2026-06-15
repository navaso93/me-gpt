from collections import Counter
from dataclasses import dataclass
import math
import re

from src.ingest import Document


TOKEN_PATTERN = re.compile(r"[a-z0-9+#.-]+")
STOP_WORDS = {
    "a",
    "about",
    "and",
    "are",
    "did",
    "does",
    "for",
    "has",
    "have",
    "is",
    "marc",
    "me",
    "of",
    "s",
    "the",
    "to",
    "what",
    "which",
    "with",
}


@dataclass(frozen=True)
class SearchResult:
    document: Document
    score: float


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in TOKEN_PATTERN.findall(text.lower())
        if token not in STOP_WORDS
    ]


class LexicalRetriever:
    """Small BM25-style retriever suitable for the first portfolio MVP."""

    def __init__(self, documents: list[Document]):
        self.documents = documents
        self.tokens = [
            tokenize(f"{document.title} {document.content}") for document in documents
        ]
        self.average_length = (
            sum(map(len, self.tokens)) / len(self.tokens) if self.tokens else 0
        )
        self.document_frequency = Counter(
            token for tokens in self.tokens for token in set(tokens)
        )

    def search(
        self, query: str, limit: int = 3, minimum_score: float = 0.2
    ) -> list[SearchResult]:
        query_tokens = tokenize(query)
        scored = []
        for document, tokens in zip(self.documents, self.tokens):
            score = self._score(query_tokens, tokens)
            if score >= minimum_score:
                scored.append(SearchResult(document=document, score=score))
        return sorted(scored, key=lambda result: result.score, reverse=True)[:limit]

    def _score(self, query_tokens: list[str], tokens: list[str]) -> float:
        if not tokens or not self.documents:
            return 0
        frequencies = Counter(tokens)
        score = 0.0
        for token in set(query_tokens):
            document_frequency = self.document_frequency[token]
            inverse_frequency = math.log(
                1 + (len(self.documents) - document_frequency + 0.5)
                / (document_frequency + 0.5)
            )
            frequency = frequencies[token]
            length_adjustment = 1.2 * (
                0.25 + 0.75 * len(tokens) / self.average_length
            )
            score += inverse_frequency * frequency * 2.2 / (
                frequency + length_adjustment
            )
        return score
