"""
    The CrawlerResponseProcessor processes HTTP responses obtained by the Crawler class. It extracts content, parses it,
    cleans it, validates it, and returns structured data (e.g., URLs or extracted metadata).

    Methods:
        process_response(response: object) -> dict | None:
            Processes the response through extraction, parsing, cleaning, and validation.

        _extract_content(response: object) -> str | dict:
            Extracts raw content from the HTTP response.

        _parse_content(raw_content: str | dict) -> dict:
            Parses the extracted content into structured data.

        _clean_data(parsed_data: dict) -> dict:
            Cleans and normalizes parsed data.

        _validate_data(cleaned_data: dict) -> bool:
            Validates cleaned data before returning it.
"""
class CrawlerResponseProcessor:
    def __init__(self, logger, parser, cleaner, validator):
        """
        Args:
            logger (object): Logger object for debugging and info logs.
            parser (object): Parser object to handle data extraction.
            cleaner (object): Cleaner object to sanitize parsed data.
            validator (object): Validator object to ensure data validity.

        Returns:
            None

        Preconditions:
            - logger, parser, cleaner, and validator must be valid and non-null.

        Postconditions:
            - Dependencies are assigned to internal attributes.
        """
        self._logger = logger
        self._parser = parser
        self._cleaner = cleaner
        self._validator = validator

    def process_response(self, response):
        """
        Processes the web crawler response through extraction, parsing, cleaning, and validation.

        Args:
            response (object): HTTP response object (e.g., from requests or aiohttp).

        Returns:
            dict | None: Cleaned and validated data dictionary or None if validation fails.

        Preconditions:
            - response must contain headers and either .json() or .text content.

        Postconditions:
            - Returns structured data if successful.

        Raises:
            - Catches and logs all internal exceptions.
        """
        try:
            raw_content = self._extract_content(response)
            parsed_data = self._parse_content(raw_content)
            cleaned_data = self._clean_data(parsed_data)
            validated_data = self._validate_data(cleaned_data)

            if validated_data:
                self._logger.info("Successfully processed response")
                return cleaned_data
            else:
                self._logger.warning("Data validation failed.")
                return None
        except Exception as e:
            self._logger.error(f"Error processing response: {e}")
            return None

    # ----- Private responsibilities -----

    def _extract_content(self, response):
        """
        Extracts content from the response.

        Args:
            response (object): HTTP response object.

        Returns:
            str | dict: Raw content (JSON or text).

        Preconditions:
            - response.headers must include 'Content-Type'.

        Postconditions:
            - Extracted raw content is returned.
        """
        self._logger.debug("Extracting response content")
        content_type = response.headers.get('Content-Type', '')
        if "application/json" in content_type:
            return response.json()
        else:
            return response.text

    def _parse_content(self, raw_content):
        """
        Parses raw response content into structured data.

        Args:
            raw_content (str | dict): Raw HTML or JSON content.

        Returns:
            dict: Parsed structured data.

        Preconditions:
            - raw_content is not None.

        Postconditions:
            - Parsed data is returned.
        """
        self._logger.debug("Parsing content")
        return self._parser.parse(raw_content)

    def _clean_data(self, parsed_data):
       """
        Cleans and normalizes parsed data.

        Args:
            parsed_data (dict): Parsed structured data.

        Returns:
            dict: Cleaned data.

        Preconditions:
            - parsed_data must be a dictionary.

        Postconditions:
            - Data is cleaned and returned.
        """
       self._logger.debug("Cleaning parsed data")
       return self._cleaner.clean(parsed_data)
    
    def _validate_data(self, cleaned_data):
        """
        Validates cleaned data.

        Args:
            cleaned_data (dict): Data to validate.

        Returns:
            bool: True if valid, False otherwise.

        Preconditions:
            - cleaned_data must be a dictionary.

        Postconditions:
            - Returns True if data passes validation, else False.
        """
        self._logger.debug("Validating cleaned data")
        return self._validator.is_valid(cleaned_data)
