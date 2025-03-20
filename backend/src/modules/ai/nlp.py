import csv
import os
import re
from typing import Set, List, Dict, Any


class NLP:
    """
    A class to process text data in CSV files by removing specified stopwords.

    This class provides functionality to clean text data in CSV files
    by removing commonly occurring words that add little meaning (stopwords).
    """

    def __init__(self, stop_words: Set[str] | None = None) -> None:
        """
        Initialize the text processor with optional custom stopwords.

        Args:
            stop_words (Set[str], optional): A set of words to be removed from the text.
                                            Defaults to {"the", "and", "or"} if not provided.
        """
        self.stop_words = stop_words or {"the", "or", "and", "a", "an"}

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

        # Check if the file exisits
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        # Sequentially process csv
        rows = self._read_csv(csv_path)
        cleaned_rows = self._process_content(rows)
        self._write_csv(csv_path, cleaned_rows)

        print(f"Cleaned CSV '{csv_path}' has been generated.")

        pass

    def _read_csv(self, csv_path: str) -> Dict[str, Any]:
        """
        Read and validate a CSV file.

        This method reads the CSV file at the specified path, validates that it contains
        the required columns, and returns the contents as a dictionary containing the
        fieldnames and rows.

        Args:
            csv_path (str): The path to the CSV file to read.

        Returns:
            Dict[str, Any]: A dictionary containing:
                            - 'fieldnames': The column names from the CSV
                            - 'rows': A list of dictionaries representing each row

        Raises:
            ValueError: If the CSV file does not contain all required columns
                       ('id', 'content', 'url').
        """
        with open(csv_path, "r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames

            # Validate that columns are the required metadata
            required_columns = {"id", "content", "url"}
            if not fieldnames or not required_columns.issubset(set(fieldnames)):
                raise ValueError(
                    f"CSV must contain columns: {', '.join(required_columns)}"
                )
            # Get all the rows
            rows = list(reader)

        return {"fieldnames": fieldnames, "rows": rows}

    def _process_content(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process the content field of each row to remove stopwords.

        This method takes the rows from a CSV file and processes the 'content' field
        of each row by removing all occurrences of stopwords defined in self.stop_words.

        Args:
            data (Dict[str, Any]): A dictionary containing:
                                   - 'fieldnames': The column names from the CSV
                                   - 'rows': A list of dictionaries representing each row

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the processed rows
                                 with stopwords removed from the 'content' field.
        """
        cleaned_rows = []
        for row in data["rows"]:
            text = row.get("content", "")
            if text:
                # Tokenize and filter
                words = re.findall(r"\w+", text, flags=re.IGNORECASE)
                filtered_words = [
                    word for word in words if word.lower() not in self.stop_words
                ]

                cleaned_text = " ".join(filtered_words)
                row["content"] = cleaned_text

            cleaned_rows.append(row)
        return cleaned_rows

    def _write_csv(
        self, csv_path: str, rows: List[Dict[str, Any]], fieldnames=None
    ) -> None:
        """
        Write processed rows back to a CSV file.

        This method writes the processed rows back to the CSV file, overwriting the original.

        Args:
            csv_path (str): The path to the CSV file to write to.
            rows (List[Dict[str, Any]]): A list of dictionaries representing the rows to write.
            fieldnames (List[str], optional): The column names to use in the CSV.
                                             If None, uses the keys from the first row
                                             or defaults to ["id", "content", "url"].

        Note:
            This method will overwrite the existing file at csv_path.
        """
        if not fieldnames:
            fieldnames = list(rows[0].keys()) if rows else ["id", "content", "url"]

        with open(csv_path, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
