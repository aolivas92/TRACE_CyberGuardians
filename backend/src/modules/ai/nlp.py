class NLP:
    def subroutine(self, csv_path: str) -> None:
        """
        Processes a CSV file by removing specified stopwords from the 'content' column.

        This function reads a CSV file, removes common stopwords defined by class as
        `self.stop_words: set[str]` from the 'content' field, and overwrites the original
        file with the cleaned text.

        Args:
            csv_path (str): The file path to the CSV file.

        Raises:
            FileNotFoundError: If the specified CSV file does not exist.
            ValueError: If the CSV file does not contain the required columns ('id', 'content', 'url').

        Behavior:
            - Reads the CSV file and ensures it contains the required columns.
            - Cleans the 'content' field by removing predefined stopwords.
            - Saves the modified data back to the original CSV file.

        Example:
            Given a CSV file with the following content:

            ```
            id,content,url
            1,"The quick brown fox jumps over the lazy dog","http://example.com"
            2,"This is an example and a test","http://test.com"
            ```

            The function will produce:

            ```
            id,content,url
            1,"quick brown fox jumps over lazy dog","http://example.com"
            2,"This is an example a test","http://test.com"
            ```

        Note:
            This function modifies the original file in place.
        """
        pass
