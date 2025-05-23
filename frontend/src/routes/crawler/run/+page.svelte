<script>
	import { Button } from '$lib/components/ui/button/index.js';
	import { goto } from '$app/navigation';
	import { Progress } from '$lib/components/ui/progress/index.js';
	import { onMount, onDestroy } from 'svelte';
	import { serviceStatus } from '$lib/stores/projectServiceStore.js';
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import Spinner from '$lib/components/ui/spinner/Spinner.svelte';
	import Table from '$lib/components/ui/table/Table.svelte';
	import Alert from '$lib/components/ui/alert/Alert.svelte';
	import { derived, get, writable } from 'svelte/store';
	import { serviceResults } from '$lib/stores/serviceResultsStore.js';
	import { toast } from 'svelte-sonner';
	import { connectToCrawlerWebSocket, closeCrawlerWebSocket } from '$lib/services/crawlerSocket';
	import {
		scanProgress,
		scanPaused,
		startScanProgress,
		stopScanProgress,
		pauseScan,
		resumeScan
	} from '$lib/stores/scanProgressStore.js';

	const { data } = $props();
	let showStopDialog = $state(false);
	let intervalId;

	// Derived stores
	const crawlerResults = derived(serviceResults, ($serviceResults) => $serviceResults.crawler);
	const dynamicColumns = derived(crawlerResults, ($crawlerResults) =>
		$crawlerResults.length > 0
			? Object.keys($crawlerResults[0]).map((key) => ({
					key,
					label: key
						.replace(/([a-z])([A-Z])/g, '$1 $2')
						.split('_')
						.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
						.join(' ')
				}))
			: []
	);
	const showProgress = derived(
		[serviceStatus, crawlerResults],
		([$serviceStatus, $crawlerResults]) =>
			$serviceStatus.status === 'running' && $crawlerResults.length > 0
	);

	const currentStep = derived(serviceStatus, ($serviceStatus) =>
		$serviceStatus.status === 'running' || $serviceStatus.status === 'paused'
			? 'running'
			: $serviceStatus.status === 'completed'
				? 'results'
				: 'config'
	);

	// Fetch results from the server
	async function fetchResults(jobId) {
		try {
			const res = await fetch(`http://localhost:8000/api/crawler/${jobId}/results`);
			const response = await res.json();
			const parsed = Array.isArray(response) ? response : (response.results ?? []);

			// Set into shared store under "crawler"
			serviceResults.update((r) => ({
				...r,
				crawler: parsed
			}));
		} catch (e) {
			console.error('Failed to fetch crawler results:', e);
		}
	}

	// WebSocket connection
	$effect(() => {
		if ($currentStep === 'results' && $crawlerResults.length === 0) {
			const jobId = localStorage.getItem('currentCrawlerJobId');
			if (jobId) {
				console.log('[Fetcher] Fetching results for job:', jobId);
				fetchResults(jobId);
			}
		}
	});

	const togglePause = async () => {
		if ($scanPaused) {
			await resumeScan('crawler');
		} else {
			await pauseScan('crawler');
		}
	};

	function handleStopCancel() {
		showStopDialog = false;
	}

	function saveCheckpoint() {
		const jobId = localStorage.getItem('currentCrawlerJobId');
		if (!jobId) {
			toast.error('No job ID found.');
			return;
		}

		const data = get(serviceResults).crawler;
		if (!data || data.length === 0) {
			toast.error('No results to checkpoint.');
			return;
		}

		localStorage.setItem(`checkpoint_${jobId}`, JSON.stringify(data));
		toast.success('Checkpoint saved!', {
			description: `Saved at ${new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })}`
		});
		console.log(`[Checkpoint] Saved for job ${jobId}`);
	}

	async function handleStopConfirm() {
		showStopDialog = false;
		stopScanProgress();
		closeCrawlerWebSocket();

		// Get the job id
		const jobId = localStorage.getItem('currentCrawlerJobId');
		if (!jobId) {
			console.error('No Crawler Job Id found in local storage');
		}

		// Clear app state
		serviceResults.update((r) => ({ ...r, crawler: [] }));
		serviceStatus.set({ status: 'idle', serviceType: null, startTime: null });
		localStorage.removeItem('currentCrawlerJobId');

		// Tell the backend to stop
		try {
			const res = await fetch(`http://localhost:8000/api/crawler/${jobId}/stop`, {
				method: 'POST'
			});
			if (res.ok) {
				console.log('Crawler job stopped.');
			} else {
				console.error('Failed to stop crawler job:', await res.text());
			}
		} catch (e) {
			console.error('Failed to stop crawler:', e);
		}

		console.log('[Stop] Service state');
		goto('/dashboard');
	}

	function handleRestart() {
		stopScanProgress();

		// Reset the service results and status
		serviceResults.update((r) => ({ ...r, crawler: [] }));
		serviceStatus.set({ status: 'idle', serviceType: null, startTime: null });
		localStorage.removeItem('currentCrawlerJobId');

		console.log('[Restart] Service state');
		goto('/crawler/config');
	}

	function handleClearJob() {
		const jobId = localStorage.getItem('currentCrawlerJobId');
		if (jobId) {
			localStorage.removeItem(`checkpoint_${jobId}`);
			localStorage.removeItem('currentCrawlerJobId');
		}
		serviceResults.update((r) => ({ ...r, crawler: [] }));
		serviceStatus.set({ status: 'idle', serviceType: null, startTime: null });
		goto('/crawler/config');
		console.log('[Clear Job] Service state and local storage cleared');
	}

	async function handleExport() {
		const jobId = localStorage.getItem('currentCrawlerJobId');
		if (!jobId) {
			console.log('Crawler job ID not found.');
			return;
		}

		let data = get(serviceResults).crawler;

		// If not in memory, fetch from server
		if (!data || data.length === 0) {
			console.log('[Export] No results found in store. Fetching from API...');
			try {
				const res = await fetch(`http://localhost:8000/api/crawler/${jobId}/results`);
				if (!res.ok) throw new Error('Failed to fetch crawler results.');
				const { results = [] } = await res.json();
				data = results;

				// OPTIONAL: Update the store if you want the UI to react too
				serviceResults.update((r) => ({ ...r, crawler: data }));
			} catch (error) {
				console.error('[Crawler Export Error]', error);
				toast.error('Failed to fetch crawler results.');
				return;
			}
		}

		if (!data || data.length === 0) {
			toast.error('No results available for export.');
			return;
		}

		// Build CSV
		const exportFields = [
			'url',
			'parentUrl',
			'title',
			'wordCount',
			'charCount',
			'linksFound',
			'error'
		];
		const headers = [
			'URL',
			'Parent URL',
			'Title',
			'Word Count',
			'Character Count',
			'Links Found',
			'Error'
		];

		const csvRows = [
			headers.join(','), 
			...data.map((row) => exportFields.map((key) => JSON.stringify(row[key] ?? '')).join(','))
		];

		const csvContent = csvRows.join('\n');
		const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
		const url = URL.createObjectURL(blob);

		const a = document.createElement('a');
		a.href = url;
		a.download = `crawler_${jobId}_results.csv`;
		document.body.appendChild(a);
		a.click();
		a.remove();

		URL.revokeObjectURL(url);
	}

	// Restore checkpoint on mount
	onMount(() => {
		const jobId = localStorage.getItem('currentCrawlerJobId');
		if (jobId && get(serviceStatus).status !== 'completed') {
			connectToCrawlerWebSocket(jobId);
		}

		intervalId = setInterval(() => {
			const jobId = localStorage.getItem('currentCrawlerJobId');
			const status = get(serviceStatus);

			// Do not save checkpoints after scan is completed or idle
			if (!jobId || (status.status !== 'running' && status.status !== 'paused')) return;

			const data = get(serviceResults).crawler;
			if (data.length > 0) {
				localStorage.setItem(`checkpoint_${jobId}`, JSON.stringify(data));
				console.log(`[Auto] Checkpoint saved for job ${jobId}`);
			}
		}, 15000);
	});

	onDestroy(() => {
		clearInterval(intervalId);
		closeCrawlerWebSocket();
	});
</script>

<svelte:head>
	<title>Crawler Run | TRACE</title>
</svelte:head>

<div class="crawler-run">
	<div class="title-section">
		<div class="title">
			{$currentStep === 'running' ? 'Crawler Scanning' : 'Crawler Results'}
		</div>
		<StepIndicator status={$currentStep} />
	</div>

	<div class="table">
		{#if $showProgress || $serviceStatus.status === 'completed' || $serviceStatus.status === 'paused'}
			<div class="progress-bar-container">
				<div class="progress-info">
					<div class="text-sm font-medium">Progress</div>
					<div class="text-2xl font-bold">{$scanProgress}% scanned</div>
				</div>
				<Progress value={$scanProgress} max={100} class="w-[100%]" />
			</div>
		{:else}
			<Spinner />
		{/if}

		<Table data={$crawlerResults} columns={$dynamicColumns} />
	</div>

	<div class="button-section">
		<div class="left-buttons">
			{#if $serviceStatus.status === 'completed'}
				<Button
					onclick={handleRestart}
					variant="default"
					size="default"
					class="restart-button"
					aria-label="Restart the scan"
					title="Click to restart the scan"
				>
					Restart
				</Button>
				<Button
					onclick={handleExport}
					variant="secondary"
					size="default"
					class="view-all-results"
					aria-label="Export results"
					title="Click to export crawler results"
				>
					Export Results
				</Button>
			{:else if $serviceStatus.status === 'running' || $serviceStatus.status === 'paused'}
				<Button
					onclick={togglePause}
					variant="secondary"
					size="default"
					class="pause-button"
					aria-label={$scanPaused ? 'Resume the scan' : 'Pause the scan'}
					title={$scanPaused ? 'Click to resume the scan' : 'Click to pause the scan'}
				>
					{#if $scanPaused}
						Resume
					{:else}
						Pause
					{/if}
				</Button>

				<Button
					onclick={saveCheckpoint}
					variant="secondary"
					size="default"
					class="save-checkpoint"
					aria-label="Save checkpoint"
					title="Checkpoint"
				>
					Save Checkpoint
				</Button>
			{/if}
		</div>

		<div class="right-buttons">
			{#if $serviceStatus.status === 'running' || $serviceStatus.status === 'paused'}
				<Button
					onclick={() => (showStopDialog = true)}
					variant="destructive"
					size="default"
					class="stop-button"
					aria-label="Stop the scan"
					title="Click to stop the scan"
				>
					Stop
				</Button>
			{:else if $serviceStatus.status === 'error'}
				<Button
					onclick={handleClearJob}
					variant="destructive"
					size="default"
					class="clear-button"
					aria-label="Clear error state"
					title="Clear scan state and try again"
				>
					Clear Job
				</Button>
			{/if}
		</div>
	</div>

	<Alert
		isOpen={showStopDialog}
		title="Are you absolutely sure?"
		message="This action cannot be undone. This will permanently stop the crawler and save current progress."
		onCancel={handleStopCancel}
		onContinue={handleStopConfirm}
	/>
</div>

<style>
	.crawler-run {
		display: flex;
		margin-left: 4.5rem;
		height: 100vh;
		flex-direction: column;
	}
	.title-section {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		width: 100%;
		max-height: fit-content;
		padding-right: 3rem;
	}
	.title {
		font-size: 2rem;
		font-style: normal;
		font-weight: 600;
		padding-left: 3rem;
		padding-top: 3rem;
	}
	.table {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100%;
	}
	.button-section {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		padding: 0rem 8rem 3rem 8rem;
	}

	.left-buttons,
	.right-buttons {
		display: flex;
		flex-direction: row;
		gap: 1rem;
	}

	.progress-bar-container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		max-width: 100%;
		width: 80%;
		margin: 0 auto;
		padding-left: 3rem;
		padding-right: 3rem;
		padding-top: 1rem;
	}
	.progress-info {
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
		width: 100%;
	}
</style>
