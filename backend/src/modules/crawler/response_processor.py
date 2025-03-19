class CrawlerResponseProcessor:
    def __init__(self, logger, parser, cleaner, validator):
        """
        Initializes the response processor with dependencies.

        :param logger: Logger object for debugging and info logs.
        :param parser: Parser object to handle data extraction.
        :param cleaner: Cleaner object to sanitize parsed data.
        :param validator: Validator object to ensure data validity.
        """
        self._logger = logger
        self._parser = parser
        self._cleaner = cleaner
        self._validator = validator

    def process_response(self, response):
        """
        Public method to process the web crawler response.

        :param response: HTTP response object (e.g., from requests or aiohttp).
        :return: Dict or list with processed data or None.
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
        Private method to extract content from the response.
        Handles different content-types (HTML, JSON, etc.).
        """
        self._logger.debug("Extracting response content")
        content_type = response.headers.get('Content-Type', '')
        if "application/json" in content_type:
            return response.json()
        else:
            return response.text

    def _parse_content(self, raw_content):
        """
        Private method to parse raw response content into structured data.
        """
        self._logger.debug("Parsing content")
        return self._parser.parse(raw_content)

    def _clean_data(self, parsed_data):
        """
        Private method to clean and normalize parsed data.
        """
        self._logger.debug("Cleaning parsed data")
        return self._cleaner.clean(parsed_data)

    def _validate_data(self, cleaned_data):
        """
        Private method to validate cleaned data before storage/use.
        """
        self._logger.debug("Validating cleaned data")
        return self._validator.is_valid(cleaned_data)
