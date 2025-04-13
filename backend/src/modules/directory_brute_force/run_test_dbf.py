import asyncio

from httpmock import AsyncHttpClient
from dbf_manager import DirectoryBruteForceManager
from dbf_response_processor import ResponseProcessor

async def run_directory_brute_force_test():
    # Setup
    client = AsyncHttpClient()
    manager = DirectoryBruteForceManager(http_client=client)

    # Sample wordlist to test existing and non-existing endpoints
    wordlist = [
        '',  # root
        'level1/page1',
        'level1/page2',
        'level2/page1',
        'level2/page2',
        'level2/page3',
        'notfound'
    ]

    # Configure scan
    manager.configure_scan(
        target_url='http://localhost:5002',
        wordlist=wordlist,
        hide_status=[404],
        show_only_status=[200],
        length_filter=0,
        attempt_limit=-1
    )

    # Start scanning
    await manager.start_scan()

    # Results
    print("\n--- Filtered Results ---")
    for result in manager.get_filtered_results():
        print(result)

    print("\n--- Metrics ---")
    print(manager.get_metrics())


if __name__ == "__main__":
    asyncio.run(run_directory_brute_force_test())
