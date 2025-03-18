class WebScraper:
    """
    this class is responsible for extracting the data from a HTML
    file and structuring it to be used by NLP Processor class
    and the ML algorithm class


    Attributes: N/A

    Methods/functions:

    Extract_data: Extract relevant URLs from HTML file as well as any
    extract all words associated with logos, labels and class titles

    create_CSV: To pass the results derived from the data extraction, it
    will be put into a CSV file fomrat to be easy to read by other classes

    scrape_parallel: WHen requested, it allows the class to do parallel
    scraping 
    
    process_batches: WHen requested this will allow web scraping to be 
    done in batches

    provide_results: gives the results that have been gathered from the 
    web scraper after fomratting it into a CSV file format

    create_URL_hierarchy_tree: organize URLs into a hierarchy tree
    structure to facilitate structured exploration, enabling efficient
    parallel processing and CSV generation    

    Notes:
    For the implementation of parallel scraping, aoihttp will be used. There
    will be the usage of BeautifulSoup for the extraction of data from 
    HTML files. Also, the library, Pandas, may be considered since it makes 
    the implementation of create_CSV a lot easier.
    """
    
