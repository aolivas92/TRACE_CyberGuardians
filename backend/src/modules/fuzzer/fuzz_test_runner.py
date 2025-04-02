import asyncio
from FuzzerManager import FuzzerManager

async def run_fuzzing_test():
    fuzzer = FuzzerManager()

    fuzzer.configure_fuzzing(
        target_url="http://www.fragrancenet.com/search",
        http_method="GET",
        headers={"User-Agent": "Mozilla/5.0"},
        cookies={},
        proxy=None,
        body_template={},  # Not used in GET
        parameters=["q"],
        payloads=["gucci", "versace", "boss", "<script>alert(1)</script>"]
    )

    print("[*] Starting fuzzing run...")
    await fuzzer.start_fuzzing()

    results = fuzzer.get_filtered_results()

    with open("results_fuzzer.txt", "w", encoding="utf-8") as f:
        for r in results:
            f.write(f"URL: {r['url']} | Status: {r['status_code']} | Length: {r['length']}")
            f.write(f"Snippet: {r['body_snippet'][:100]}...\n")

if __name__ == "__main__":
    asyncio.run(run_fuzzing_test())