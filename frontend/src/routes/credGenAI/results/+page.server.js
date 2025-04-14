export async function load({ fetch, url }) {
	const jobId = url.searchParams.get('jobId');

	if (!jobId) {
		console.warn('[Fetcher] No jobId provided in URL.');
		return {
			tableData: [],
			tableColumns: []
		};
	}

	console.log('[Fetcher] Fetching results for job:', jobId);

	try {
		const res = await fetch(`http://127.0.0.1:8000/api/ml/${jobId}/results`);
		const json = await res.json();

		const tableData = json.results ?? [];
		const tableColumns = [
			{ key: 'id', label: 'ID' },
			{ key: 'username', label: 'Username' },
			{ key: 'username_score', label: 'Username Score' },
			{ key: 'password', label: 'Password' },
			{ key: 'is_secure', label: 'Secure?' },
			{ key: 'password_evaluation', label: 'Evaluation' }
		];

		console.log('[DataTable] Results received:', tableData.length);

		return { tableData, tableColumns };
	} catch (e) {
		console.error('[Fetcher] Failed to load ML results:', e);
		return {
			tableData: [],
			tableColumns: []
		};
	}
}
