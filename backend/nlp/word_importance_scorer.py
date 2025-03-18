from enum import Enum
import math
import numpy as np


class ImportanceType(Enum):
    """
    Enumeration for different word importance scoring methods.
    """

    TF_IDF = "tf_idf"
    PREDEFINED = "predefined"
    NER = "ner"


class WordImportanceScorer:
    """
    Handles different word importance scoring methods.
    """

    def __init__(self) -> None:
        self.predefined_scores = {
            "very": 1,
            "important": 5,
            "word": 3,
            "the": 0,
            "is": 1,
            "critical": 5,
        }
        self.named_entities = {
            "Netflix",
            "Sundar",
            "Pichai",
            "NASA",
            "Google",
            "Microsoft",
            "Paris",
            "London",
            "Python",
            "Amazon",
            "Apple",
            "January",
            "February",
            "2024",
            "President",
        }

    def compute_tf(self, words: list[str]) -> dict:
        word_counts = {}
        total_words = len(words)
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        return {word: count / total_words for word, count in word_counts.items()}

    def compute_idf(self, words: list[str]) -> dict:
        word_counts = {}
        total_words = len(words)
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        return {
            word: np.log((total_words + 1) / (count + 1)) + 1
            for word, count in word_counts.items()
        }

    def compute_tf_idf(self, words: list[str]) -> dict:
        tf_scores = self.compute_tf(words)
        idf_scores = self.compute_idf(words)
        return {word: tf_scores[word] * idf_scores[word] for word in words}

    def score_predefined(self, words: list[str]) -> dict:
        return {word: self.predefined_scores.get(word, 0.5) for word in words}

    def score_ner(self, words: list[str]) -> dict:
        return {word: 2.0 if word in self.named_entities else 0.5 for word in words}

    def get_importance_scores(self, words: list[str], method: ImportanceType) -> dict:
        match method:
            case ImportanceType.TF_IDF:
                return self.compute_tf_idf(words)
            case ImportanceType.PREDEFINED:
                return self.score_predefined(words)
            case ImportanceType.NER:
                return self.score_ner(words)
            case _:
                raise ValueError(f"Unsupported ImportanceType selected: {method}")
