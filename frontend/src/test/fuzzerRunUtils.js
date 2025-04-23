export function saveCheckpoint(jobId, data, toast = console) {
	if (!jobId) {
		toast.error('No job ID found.');
		return false;
	}

	if (!Array.isArray(data) || data.length === 0) {
		toast.error('No results to checkpoint.');
		return false;
	}

	localStorage.setItem(`checkpoint_${jobId}`, JSON.stringify(data));
	toast.success('Checkpoint saved!', {
		description: `Saved at ${new Date().toLocaleTimeString([], {
			hour: 'numeric',
			minute: '2-digit',
			hour12: true
		})}`
	});
	return true;
}

export async function exportFuzzerResults(jobId, fetchFn = fetch) {
	if (!jobId) throw new Error('No job ID found.');

	const res = await fetchFn(`http://localhost:8000/api/fuzzer/${jobId}/results`);
	if (!res.ok) throw new Error('Failed to fetch fuzzer results.');

	const { results = [] } = await res.json();
	const exportFields = ['id', 'response', 'payload', 'length', 'error'];
	const headers = ['ID', 'Response', 'Payload', 'Length', 'Error'];

	const csvRows = [
		headers.join(','),
		...results.map(row =>
			exportFields.map(key => JSON.stringify(row[key] ?? '')).join(',')
		)
	];

	return csvRows.join('\n');
}