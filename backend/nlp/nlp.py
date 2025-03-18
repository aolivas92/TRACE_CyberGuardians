from nlp.word_importance_scorer import WordImportanceScorer, ImportanceType


class NLP:
    """
    Handles text preprocessing and analysis for AI credential generation.

    This class provides methods for processing natural language text data to prepare
    it for AI credential generation systems. It includes functionality for text
    normalization, tokenization, and various text transformations.

    Attributes:
        No public attributes.

    Methods:
        normalize(text_to_normalize: list[str]) -> None:
            Normalizes the input text in place.

        trim_short_words(text: list[str]) -> None:
            Removes words shorter than a minimum threshold from the text list.

        break_compound_words(text: list[str]) -> None:
            Splits compound words connected by apostrophes.

        remove_delimeters(text: list[str]) -> None:
            Removes common articles and delimiter words from the text list.

    Notes:
        This class doesn't inherit from any superclass and doesn't define
        any private responsibilities outside of its methods.
    """

    def __init__(
        self,
        MIN_WORD_SIZE: int = 3,
        MIN_IMPORTANCE_RATING: float = 0.1,
        importance_type: ImportanceType = ImportanceType.TF_IDF,
    ):
        self.MIN_WORD_SIZE = MIN_WORD_SIZE
        self.MIN_IMPORTANCE_RATING = MIN_IMPORTANCE_RATING
        self.article_dictionary = {"a", "an", "the"}
        self.compound_word_dictionary = {
            "i'm": ["I", "am"],
            "you're": ["you", "are"],
            "it's": ["it", "is"],
            "don't": ["do", "not"],
            "can't": ["can", "not"],
            "isn't": ["is", "not"],
            "won't": ["will", "not"],
            "didn't": ["did", "not"],
            "we're": ["we", "are"],
            "they're": ["they", "are"],
            "I'll": ["I", "will"],
            "you'll": ["you", "will"],
            "he'll": ["he", "will"],
            "she'll": ["she", "will"],
            "we'll": ["we", "will"],
            "they'll": ["they", "will"],
            "I've": ["I", "have"],
            "you've": ["you", "have"],
            "we've": ["we", "have"],
            "they've": ["they", "have"],
            "he's": ["he", "is"],
            "she's": ["she", "is"],
            "that's": ["that", "is"],
            "what's": ["what", "is"],
            "let's": ["let", "us"],
            "there's": ["there", "is"],
            "who's": ["who", "is"],
            "how's": ["how", "is"],
        }
        self.importance_type = importance_type
        self.importance_scorer = WordImportanceScorer()

    def normalize(self, text_to_normalize: list[str]) -> None:
        """
        Normalize the input text, in place.

        This method performs text normalization operations on each string in the provided list,
        modifying the list contents directly without returning a new object. Normalization
        may include operations such as:
        - Converting text to lowercase
        - Removing special characters
        - Standardizing whitespace
        - Removing accents/diacritics
        - Expanding contractions
        - Standardizing text encodings

        Args:
            text_to_normalize (list[str]): A list of strings to be normalized.
                This list will be modified in place.

        Returns:
            None: This method modifies the input list in place and does not return a value.

        Raises:
            TypeError: If the input is not a list of strings.
            ValueError: If normalization fails for any string in the list.

        Example:
            >>> processor = NLP()
            >>> texts = ["Hello, World!", "IT'S   a Test123"]
            >>> processor.normalize(texts)
            >>> texts
            ['hello world', 'its a test123']
        """
        if not isinstance(text_to_normalize, list) or not all(
            isinstance(s, str) for s in text_to_normalize
        ):
            raise TypeError("Input must be a list of strings.")
        text_to_normalize[:] = [word.lower() for word in text_to_normalize]

        for i, text in enumerate(text_to_normalize):
            normalized = " ".join(text.split())

            final_text = ""
            for char in normalized:
                if char.isalnum() or char.isspace():
                    final_text += char
            text_to_normalize[i] = final_text

    def trim_short_words(self, text: list[str]) -> None:
        """
        Removes words shorter than a minimum size from the given text list, and a low importance rating.

        This method modifies the input list in place, removing any strings that are
        shorter than the minimum word size threshold defined by the class.

        Args:
            text (list[str]): A list of strings to be processed. Must not be None
                and must not be empty.

        Returns:
            None: This method modifies the input list in place.

        Preconditions:
            - The input text list must not be None.
            - The input text list must not be empty.

        Postconditions:
            - After execution, all strings remaining in the text list will have a length
              greater than or equal to the minimum word size.
            - The method does not return a value.

        Raises:
            ValueError: If the input is None or empty.
        """
        if text is None or not text:
            raise ValueError(
                "Input text list must be a valid value (not None or empty)."
            )
        importance_ratings = self.importance_scorer.get_importance_scores(
            text, self.importance_type
        )

        text[:] = [
            word
            for word in text
            if len(word) >= self.MIN_WORD_SIZE
            and importance_ratings[word] >= self.MIN_IMPORTANCE_RATING
        ]

    def break_compound_words(self, text: list[str]) -> None:
        """
        Splits compound words in the given text list.

        This method modifies the input list in place, breaking apart compound words
        that are connected with apostrophes. After execution, no apostrophes (')
        will remain in any strings within the list.

        Args:
            text (list[str]): A list of strings to be processed. Must not be None
                and must not be empty.

        Returns:
            None: This method modifies the input list in place.

        Preconditions:
            - The input text list must not be None.
            - The input text list must not be empty.

        Postconditions:
            - After execution, no string in the text list will contain apostrophes (').
            - The method does not return a value.

        Raises:
            ValueError: If the input is None or empty.
        """
        if text is None or not text:  # Check for preconditions
            raise ValueError(
                "Input text list must be a valid value (not None or empty)."
            )
        uncompounded_text = []
        text[:] = [word.lower() for word in text]  # May be redundant
        for word in text:
            if word in self.compound_word_dictionary:
                uncompounded_text.extend(self.compound_word_dictionary[word])
            else:
                uncompounded_text.append(word.replace("'", ""))

        text[:] = uncompounded_text

    def remove_delimeters(self, text: list[str]) -> None:
        """
        Removes delimiter words (articles) from the given text list.

        This method modifies the input list in place, removing any strings that are
        found in the article dictionary. After execution, no words from the article
        dictionary will remain in the text list.

        Args:
            text (list[str]): A list of strings to be processed. Must not be None
                and must contain at least one element.

        Returns:
            None: This method modifies the input list in place.

        Preconditions:
            - The input text list must not be None.
            - The input text list must contain at least one element.

        Postconditions:
            - After execution, no string in the text list will be present in the
              article dictionary.
            - The method does not return a value.

        Raises:
            ValueError: If the input is None or empty.
        """
        if text is None or not text:  # Check for preconditions
            raise ValueError(
                "Input text list must be a valid value (not None or empty)."
            )

        text[:] = [word for word in text if word.lower() not in self.article_dictionary]
