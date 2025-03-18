import unittest
from nlp import NLP


class NLPTestSuite(unittest.TestCase):
    def setUp(self):
        self.processor = NLP()

    def test_basic_removal(self):
        """Test that articles are removed from a simple sentence."""
        text = ["the", "quick", "brown", "fox", "jumps", "over", "a", "lazy", "dog"]
        self.processor.remove_delimeters(text)
        self.assertEqual(
            text, ["quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
        )

    def test_case_insensitive_removal(self):
        """Ensure case insensitivity in article removal."""
        text = ["The", "cat", "sat", "on", "An", "apple"]
        self.processor.remove_delimeters(text)
        self.assertEqual(text, ["cat", "sat", "on", "apple"])

    def test_no_articles_present(self):
        """Test when no articles are in the list (should remain unchanged)."""
        text = ["hello", "world"]
        original_text = text[:]
        self.processor.remove_delimeters(text)
        self.assertEqual(text, original_text)

    def test_only_articles(self):
        """Test when the list consists only of articles (should become empty)."""
        text = ["a", "an", "the"]
        self.processor.remove_delimeters(text)
        self.assertEqual(text, [])

    def test_invalid_input_remove_delimeters(self):
        """Test that None or an empty list raises ValueError."""
        with self.assertRaises(ValueError):
            self.processor.remove_delimeters(None)
        with self.assertRaises(ValueError):
            self.processor.remove_delimeters([])

    def test_basic_contractions(self):
        """Test common contractions being expanded correctly."""
        text = ["I'm", "happy", "because", "it's", "a", "good", "day"]
        self.processor.break_compound_words(text)
        self.assertEqual(
            text, ["I", "am", "happy", "because", "it", "is", "a", "good", "day"]
        )

    def test_mixed_case_contractions(self):
        """Ensure contractions with uppercase letters expand correctly."""
        text = ["You're", "the", "best", "and", "I'm", "proud"]
        self.processor.break_compound_words(text)
        self.assertEqual(text, ["you", "are", "the", "best", "and", "I", "am", "proud"])

    def test_no_contractions(self):
        """Test that a sentence without contractions changes to lowercase."""
        text = ["Hello", "world", "this", "is", "a", "test"]
        self.processor.break_compound_words(text)
        self.assertEqual(text, ["hello", "world", "this", "is", "a", "test"])

    def test_apostrophe_in_names(self):
        """Ensure apostrophes in names are just removed, not break incorrectly."""
        text = ["O'Connor", "D'Angelo", "it's", "important"]
        self.processor.break_compound_words(text)
        self.assertEqual(text, ["oconnor", "dangelo", "it", "is", "important"])

    def test_invalid_input_break_compound_words(self):
        """Test None or empty list raises ValueError."""
        with self.assertRaises(ValueError):
            self.processor.break_compound_words(None)
        with self.assertRaises(ValueError):
            self.processor.break_compound_words([])


if __name__ == "__main__":
    unittest.main()
