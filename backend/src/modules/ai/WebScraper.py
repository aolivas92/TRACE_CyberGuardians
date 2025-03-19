class WebScraper:
    """
    this class is responsible for extracting the data from a HTML
    file and structuring it to be used by NLP Processor class
    and the ML algorithm class


    Attributes: string for the CSV filename

    Methods/functions:
    Extract_data(self, url: str)->List[str]:
    create_CSV(self, data,Tuple[str, LIst[str], filename: str])->None: 
    scrape_parallel(self, url: str)->Tuple[str, List[str]]:
    process_batches(self, url: str)->Tuple[str, List[str]]:
    get_results(self)->str:

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
  async def extract_data(self, url: str)->List[str]:
      """
      Extract relevant URLs from HTML file as well as any
      extract all words associated with logos, labels and class titles

      Args:
        self: The class instance itself
        url:
      Returns:
        List[str]: A list of urls found in the url given
      """

  async def _process_batch(self, url: str)->Tuple[str, List[str]]:
      """
      When requested this will allow web scraping to be 
      done in batches

      Args:
        self: The class instance itself
        url: The url in the form of a string
      Returns:
        Tuple[str, List[str]]: A tuple that consists of the url and the
        urls found in the url as a list of strings

        ex. (https://en.wikipedia.org/wiki/Artificial_intelligence,
        [..., https://en.wikipedia.org/wiki/Economics] )
          
      """
  async def scrape_parallel(self, url: str)->Tuple[str, List[str]]:
      """
      When requested, it allows the class to do parallel
      scraping 

      Args: 
        self: The class instance itself
        url: The url in the form of a string
      Returns:
        Tuple[str, List[str]]: A tuple that consists of the url and the
        urls found in the url as a list of strings

        ex. (https://en.wikipedia.org/wiki/Artificial_intelligence,
        [..., https://en.wikipedia.org/wiki/Economics] )
      """
  def _get_results(self)->str:
      """
       Give the results that have been gathered from the 
       web scraper after fomratting it into a CSV file format

       Args:
         self: The class instance itself
       Returns:
         str: The filename of the CSV file
       """
  def _create_CSV(self, data: Tuple[str, List[str], filename: str])->None:
      """ 
      To pass the results derived from the data extraction, it
      will be put into a CSV file fomrat to be easy to read by other classes  
      Args:
        self: The class instance itself
        data: A tuple consisting of the url and the urls found in the url
        put in as a list of strings
        filename: The name the CSV will be given once creation is completed
      Returns:
        None: It updates the attribute to refer to the new CSV by the 
        filename given
      """
