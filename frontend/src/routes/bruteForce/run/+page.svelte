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
	import { connectToBruteForceWebSocket, closeBruteForceWebSocket } from '$lib/services/bruteForceSocket.js';
	import {
		scanProgress,
		scanPaused,
		startScanProgress,
		stopScanProgress,
		pauseScan,
		resumeScan
	} from '$lib/stores/scanProgressStore.js';

	const exporting = writable(false);

	const bruteForceResults = derived(serviceResults, ($serviceResults) => $serviceResults.bruteForce);
	const dynamicColumns = derived(bruteForceResults, ($results) =>
		$results.length > 0
			? Object.keys($results[0]).map((key) => ({
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
		[serviceStatus, bruteForceResults],
		([$status, $results]) => $status.status === 'running' && $results.length > 0
	);

	const currentStep = derived(serviceStatus, ($status) =>
		$status.status === 'running' || $status.status === 'paused'
			? 'running'
			: $status.status === 'complete'
				? 'results'
				: 'config'
	);

	function togglePause() {
		if ($scanPaused) {
			resumeScan('bruteForce');
		} else {
			pauseScan('bruteForce');
		}
	}

	function handleStopCancel() {
		showStopDialog = false;
	}

	async function handleStopConfirm() {
		showStopDialog = false;
		stopScanProgress();
		closeBruteForceWebSocket();
		const jobId = localStorage.getItem('currentBruteForceJobId');
		if (!jobId) return;

		// Clear state
		serviceResults.update((r) => ({ ...r, bruteForce: [] }));
		serviceStatus.set({ status: 'idle', serviceType: null, startTime: null });
		localStorage.removeItem('currentBruteForceJobId');

		// Send stop to backend (if needed)
		try {
			await fetch(`http://localhost:8000/api/bruteForce/${jobId}/stop`, { method: 'POST' });
		} catch (e) {
			console.error('Failed to stop brute force:', e);
		}

		goto('/dashboard');
	}

	function handleRestart() {
		stopScanProgress();
		serviceResults.update((r) => ({ ...r, bruteForce: [] }));
		serviceStatus.set({ status: 'idle', serviceType: null, startTime: null });
        scanProgress.set(0);
		localStorage.removeItem('currentBruteForceJobId');
		goto('/bruteForce/config');
	}

	async function handleExport() {
		exporting.set(true);
		try {
			const results = get(bruteForceResults);
			const headers = ["Path", "Status Code", "Response Length"];
			const csvRows = [
				headers.join(','),
				...results.map(entry => [
					`"${entry.path}"`,
					entry.status,
					entry.length
				].join(','))
			];

			const csvContent = csvRows.join("\n");
			const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = `brute_force_results.csv`;
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
		} catch (err) {
			alert('Failed to export results');
			console.error(err);
		} finally {
			exporting.set(false);
		}
	}

	let showStopDialog = $state(false);

    /* for backend
	onMount(() => {
		const jobId = localStorage.getItem('currentBruteForceJobId');
		if (jobId) {
			connectToBruteForceWebSocket(jobId);
		} else {
			console.warn('No brute force job ID found in localStorage.');
		}
	});
    */
   
    // for testing 
    onMount(() => {
	    const jobId = 'test-job-123'; // mock job ID
	    localStorage.setItem('currentBruteForceJobId', jobId);

        	// Init state
	    serviceResults.set({ bruteForce: [] });
	    serviceStatus.set({ status: 'running', serviceType: 'bruteForce', startTime: Date.now() });
	    startScanProgress();

	    // Simulate progress
	    let progress = 0;
	    const interval = setInterval(() => {
		    if (progress < 100) {
			    progress += 10;
			    scanProgress.set(progress);
		    } else {
			    clearInterval(interval);
			    serviceStatus.set({ status: 'complete', serviceType: 'bruteForce', startTime: null });
			    stopScanProgress(true);
		    }
	    }, 500);

	    // Simulate pushing new results to the store
	    const mockResults = [
		    { path: '/admin', status: 200, length: 532 },
		    { path: '/login', status: 401, length: 430 },
		    { path: '/secret', status: 403, length: 390 }
	    ];

	    let i = 0;
	    const resultInterval = setInterval(() => {
		    if (i < mockResults.length) {
			    serviceResults.update((r) => ({
				    ...r,
				    bruteForce: [...(r.bruteForce || []), mockResults[i++]]
			    }));
		    } else {
			    clearInterval(resultInterval);
		    }
	    }, 600);
    });

	onDestroy(() => {
		closeBruteForceWebSocket();
	});
</script>

<svelte:head>
	<title>Brute Force Run | TRACE</title>
</svelte:head>

<div class="bruteForce-run">
	<div class="title-section">
		<div class="title">
			{$currentStep === 'running' ? 'Brute Force Scanning' : 'Brute Force Results'}
		</div>
		<StepIndicator status={$currentStep} />
	</div>

	<div class="table">
		{#if $showProgress || $serviceStatus.status === 'complete' || $serviceStatus.status === 'paused'}
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

		<Table data={$bruteForceResults} columns={$dynamicColumns} />
	</div>

	<div class="button-section">
		<div class="button-group">
			{#if $serviceStatus.status === 'complete'}
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
					title="Click to export brute force results"
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
					onclick={() => (showStopDialog = true)}
					variant="destructive"
					size="default"
					class="stop-button"
					aria-label="Stop the scan"
					title="Click to stop the scan"
				>
					Stop
				</Button>
			{/if}
		</div>
		<div class="single-button">
			<Button
				variant="secondary"
				size="default"
				class="terminal-button"
				aria-label="Open terminal"
				title="Click to open the terminal"
			>
				Terminal
			</Button>
		</div>
	</div>

	<Alert
		isOpen={showStopDialog}
		title="Are you absolutely sure?"
		message="This action cannot be undone. This will permanently stop the brute force and save current progress."
		onCancel={handleStopCancel}
		onContinue={handleStopConfirm}
	/>
</div>

<style>
	.bruteForce-run {
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
		flex-direction: row;
		justify-content: space-between;
		width: 100%;
		padding: 0rem 8rem 3rem 8rem;
	}
	.button-group {
		display: flex;
		flex-direction: row;
		gap: 1rem;
	}
	.single-button {
		display: flex;
		flex-direction: row;
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
