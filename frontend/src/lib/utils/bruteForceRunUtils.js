export function saveCheckpointForJob(jobId, data, toast) {
	if (!jobId) {
		toast.error('No job ID found.');
		return false;
	}
	if (!data || data.length === 0) {
		toast.error('No results to checkpoint.');
		return false;
	}

	localStorage.setItem(`checkpoint_${jobId}`, JSON.stringify(data));
	toast.success('Checkpoint saved!', {
		description: `Saved at ${new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })}`
	});
	return true;
}

export function createCsvContent(results) {
	const exportFields = ['id', 'url', 'status', 'payload', 'length', 'error'];
	const headers = ['ID', 'URL', 'Status Code', 'Payload', 'Length', 'Error'];

	const csvRows = [
		headers.join(','),
		...results.map((row) => exportFields.map((key) => JSON.stringify(row[key] ?? '')).join(','))
	];

	return csvRows.join('\n');
}