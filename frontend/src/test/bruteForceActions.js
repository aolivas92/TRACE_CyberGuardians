export function saveCheckpoint(jobId, data, toast) {
	if (!jobId) {
		toast.error('No job ID found.');
		return false;
	}

	if (!Array.isArray(data) || data.length === 0) {
		toast.error('No results to checkpoint.');
		return false;
	}

	localStorage.setItem(`checkpoint_${jobId}`, JSON.stringify(data));
	toast.success('Checkpoint saved!');
	return true;
}

export async function exportResults(jobId, fetchFn = fetch) {
	if (!jobId) throw new Error('No job ID found');

	const res = await fetchFn(`http://localhost:8000/api/dbf/${jobId}/results`);
	if (!res.ok) throw new Error('Failed to fetch brute force results');

	const { results = [] } = await res.json();
	const exportFields = ['id', 'url', 'status', 'payload', 'length', 'error'];
	const headers = ['ID', 'URL', 'Status Code', 'Payload', 'Length', 'Error'];

	const csvRows = [
		headers.join(','),
		...results.map((row) => exportFields.map((key) => JSON.stringify(row[key] ?? '')).join(','))
	];
	return csvRows.join('\n');
}