import asyncio
import os
import json
from src.modules.fuzzer.fuzzer_manager import FuzzerManager

async def run_fuzzing_test():
    fuzzer = FuzzerManager()

    fuzzer.configure_fuzzing(
        target_url="https://team-9-56497.firebaseapp.com/Login",
        http_method="POST",
        headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"},
        cookies={},
        proxy=None,
        body_template={"field-r1__control": "", "field-r2__control": ""},  # Not used in GET
        parameters=["field-r1__control", "field-r2__control"],
        payloads=r"C:\Users\ricar\Documents\sw2\TRACE_CyberGuardians\backend\wordlist.txt"
    )

    print("[*] Starting fuzzing run...")
    await fuzzer.start_fuzzing()

    results = fuzzer.get_filtered_results()
    metrics = fuzzer.get_metrics()

    # Go from test/fuzzer/ -> ../../modules/fuzzer/
    fuzzer_output_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "modules", "fuzzer")
    )
    os.makedirs(fuzzer_output_path, exist_ok=True)

    # Save results file into the fuzzer folder
    results_file = os.path.join(fuzzer_output_path, "results_fuzzer.txt")


    with open(results_file, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, indent=2) + "\n")

        f.write("\n--- Fuzzing Metrics ---\n")
        f.write(f"Running Time: {metrics['running_time']:.2f} seconds\n")
        f.write(f"Processed Requests: {metrics['processed_requests']}\n")
        f.write(f"Filtered Requests: {metrics['filtered_requests']}\n")
        f.write(f"Requests/sec: {metrics['requests_per_second']:.2f}\n")

if __name__ == "__main__":
    asyncio.run(run_fuzzing_test())