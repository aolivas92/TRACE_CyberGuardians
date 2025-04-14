export async function load({ fetch, url }) {
	let jobId = url.searchParams.get('jobId');

	if (!jobId) {
		return {
			tableData: [],
			tableColumns: []
		};
	}

	console.log('[Fetcher] Fetching brute force results for job:', jobId);

	try {
		const res = await fetch(`http://127.0.0.1:8000/api/bruteForce/${jobId}/results`);
		const json = await res.json();
		console.log('[BruteForce Results]', json.results);
		return {
			tableData: json.results ?? [],
			tableColumns: [
				{ key: 'path', label: 'Path' },
				{ key: 'status', label: 'Status Code' },
				{ key: 'length', label: 'Response Length' }
			]
		};
	} catch (e) {
		console.error('Failed to load brute force results:', e);
		return {
			tableData: [],
			tableColumns: []
		};
	}
}
