class WebScraper:
    """
    This class is responsible for extracting the data from a HTML
    file and structuring it to be used by NLP Processor class
    and the ML algorithm class
    Attributes: String for the CSV filename
    Methods/functions:
    extract_data(self, session: aiohttp.ClientSession, url: str, index: int) -> Tuple[int, str, List[str]]:
    set_CSV_filename(self, data: List[Tuple[int, str, List[str] ], filename: str])->None:
    scrape_parallel(self, parallel: bool = True) -> List[Tuple[int, str, str]]:
    _process_batch(self, processed_data: List[Tuple[int, str, List[str]]], batch_size: int = 10) -> List[str]:
    get_CSV_filename(self)->str:
    Notes:
    For the implementation of parallel scraping, aoihttp will be used. There
    will be the usage of BeautifulSoup for the extraction of data from 
    HTML files. Also, the library, Pandas, may be considered since it makes 
    the implementation of create_CSV a lot easier. For all methods that can
    be done in parallel--extract_data(), scrape_parallel(), and 
    process_batches()--they will be prefixed with the key word 'async'.
    """
    def __init__(self, urls: List[str]):
        """
        initialize the class object with the urls in a list of strngs
        put them into a dictonary with the key being the url and then the 
        value being the element of the list corresponding to the url
        """
        pass

    async def extract_data(self, session: aiohttp.ClientSession, url: str, index: int) -> Tuple[int, str, List[str]]:
        """
        Extract relevant URLs from HTML file as well as any
        extract all words associated with logos, labels and class titles

        Args:
            Self: The class instance itself
            url:string variable of the url being web scraped
            index: number for formatting purposes when creating a CSV file
            session: parallel session 
        Returns:
            Tuple[int, str, List[str]]: A tuple that consists of a url and a list of urls and relevant
            metadata in the form of text found in the url given
        """      
        pass

    async def _process_batch(self, processed_data: List[Tuple[int, str, List[str]], batch_size: int = 10 ])->List[str ]:


        """
        When requested this will allow web scraping to be
        done in batches
        Args:
            Self: The class instance itself
            batch_size: size of the chunk that will be passed at once to NLP or ML, default ten
            processed_data: list of the tuple structure that has the following: the index, the url, and the words, urls, and any other information extracted
        Returns:
            List[str]: Since it is doing it in batches, it will pass the batches through smaller temporary CSV files and address them by their filename

        """
        pass

    async def scrape_parallel(self, url: str, parallel: bool = True) -> List[Tuple[int, str, List[str]]]:
        """
        When requested, it allows the class to do parallel
        scraping

        Args:
            Self: The class instance itself
            parallel: a boolean variable that checks if the parallelism will be performed
            url: string variable of the irl being web scraped
        Returns:
            List[Tuple[int, str, List[str]]]: A list where each element is a tuple that consists of the url
            and the metadata found in the url as a list of strings
        """  
        pass
    def _get_CSV_filename(self) -> str:
        """
        Give the results that have been gathered from the
        web scraper after formatting it into a CSV file format

        Args:
            Self: The class instance itself
        Returns:
            Str: The filename of the CSV file
        """
        pass



    def _set_CSV_filename(self, processed_data: List[Tuple[int, str, List[str]]], filename: str) -> None:
        """
        To pass the results derived from the data extraction, it
        will be put into a CSV file format to be easy to read by other classes 
        Args:
            Self: The class instance itself
            Proessed_data: A list with elements that is a tuple consisting of the index, content, and url
            Filename: The name the CSV will be given once creation is completed
        Returns:
            None: It updates the attribute to refer to the new CSV by the
            filename given
        """
        pass

