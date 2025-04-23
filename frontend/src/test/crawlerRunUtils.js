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
	toast.success('Checkpoint saved!', {
		description: `Saved at ${new Date().toLocaleTimeString([], {
			hour: 'numeric',
			minute: '2-digit',
			hour12: true
		})}`
	});
	return true;
}

export async function exportResults(jobId, fetchFn = fetch) {
	if (!jobId) throw new Error('No job ID found');

	const res = await fetchFn(`http://localhost:8000/api/crawler/${jobId}/results`);
	if (!res.ok) throw new Error('Failed to fetch crawler results');

	const { results = [] } = await res.json();

	const exportFields = [
		'url', 'parentUrl', 'title', 'wordCount', 'charCount', 'linksFound', 'error'
	];
	const headers = [
		'URL', 'Parent URL', 'Title', 'Word Count', 'Character Count', 'Links Found', 'Error'
	];

	const csvRows = [
		headers.join(','),
		...results.map((row) =>
			exportFields.map((key) => JSON.stringify(row[key] ?? '')).join(',')
		)
	];

	return csvRows.join('\n');
}