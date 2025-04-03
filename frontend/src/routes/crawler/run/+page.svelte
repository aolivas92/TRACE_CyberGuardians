<script>
	import { Button } from '$lib/components/ui/button/index.js';
	import { goto } from '$app/navigation';
	import { Progress } from '$lib/components/ui/progress/index.js';
	import { onMount, onDestroy } from 'svelte';
	import { serviceStatus } from '$lib/stores/projectServiceStore.js';
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import Table from '$lib/components/ui/table/Table.svelte';
	import Alert from '$lib/components/ui/alert/Alert.svelte';
	import { derived } from 'svelte/store';
	import { get } from 'svelte/store';
	import { 
		scanProgress, 
		stopScanProgress, 
		scanPaused, 
		crawlerResults,
		crawlerLogs,
		jobId,
		startScanProgress
	} from '$lib/stores/scanProgressStore.js';

	const { data } = $props();
	let value = $state(15);
	let showStopDialog = $state(false);
	let paused = $state(false);
	let tableData = $state(data.tableData);
	let logs = $state([]);
	
	// Initialize websocket connection when page loads if we have a job ID
	onMount(() => {
		// Make sure the service status is set correctly for the crawler run page
		if ($serviceStatus.serviceType !== 'crawler' || $serviceStatus.status === 'idle') {
			// Initialize service status for crawler
			serviceStatus.set({
				status: 'running',
				serviceType: 'crawler',
				startTime: new Date().toISOString()
			});
		}
		
		if (data.jobId) {
			console.log('Initializing websocket with job ID:', data.jobId);
			jobId.set(data.jobId);
			startScanProgress(data.jobId);
		} else {
			console.log('No job ID provided, using mock data');
			// Set a small initial progress to trigger loading animation if no job ID
			if ($scanProgress === 0) {
				scanProgress.set(5);
			}
		}
		
		// Subscribe to crawler results for live updates
		const unsubscribeCrawlerResults = crawlerResults.subscribe((results) => {
			console.log('Received crawler results:', results);
			if (results && results.length > 0) {
				tableData = results.map((item, index) => ({
					id: index + 1,
					url: item.url,
					title: item.title || 'No Title',
					wordCount: item.wordCount || item.word_count || 0,
					charCount: item.charCount || item.char_count || 0,
					linksFound: item.linksFound || item.links_found || 0,
					error: item.error || false
				}));
			}
		});
		
		// Subscribe to crawler logs for terminal output
		const unsubscribeCrawlerLogs = crawlerLogs.subscribe((newLogs) => {
			logs = newLogs;
		});
		
		// Also track scan progress changes for debugging
		const unsubscribeProgress = scanProgress.subscribe((value) => {
			console.log(`Progress updated to: ${value}%`);
			if (value >= 100) {
				console.log('Scan completed!');
			}
		});
		
		return () => {
			unsubscribeCrawlerResults();
			unsubscribeCrawlerLogs();
			unsubscribeProgress();
		};
	});

	// Derive current step from service status - ensure 'running' is passed to table for loading animation
	const currentStep = derived([serviceStatus, scanProgress], ([$serviceStatus, $progress]) => {
		console.log('Current service status for step calculation:', $serviceStatus, 'Progress:', $progress);
		
		if ($serviceStatus.status === 'running') {
			return 'running';
		} else if ($serviceStatus.status === 'complete') {
			return 'results';
		} else if ($serviceStatus.serviceType === 'crawler' && $progress > 0 && $progress < 100) {
			// Show as running if progress is between 0-100 even if status isn't explicitly running
			return 'running';
		} else {
			return 'config';
		}
	});

	function handleStopCancel() {
		showStopDialog = false;
	}

	function handleStopConfirm() {
		showStopDialog = false;
		stopScanProgress();

		console.log('Crawler stopped');
		console.log('Current service status:', get(serviceStatus));
		goto('/dashboard');
	}

	function handleRestart() {
		// Stop scan progress and reset all related state
		stopScanProgress();
		
		// Reset service status to idle before navigating
		serviceStatus.set({
			status: 'idle',
			serviceType: null,
			startTime: null
		});
		
		console.log('Restarting at', new Date().toISOString());
		console.log('Service status reset for restart:', get(serviceStatus));
		
		// Navigate to config page
		goto('/crawler/config');
	}
</script>

<div class="crawler-run">
	<div class="title-section">
		<div class="title">
			{$currentStep === 'running' ? 'Crawler Scanning' : 'Crawler Results'}
		</div>
		<StepIndicator status={$currentStep} />
	</div>
	<!-- Debug information - uncomment if needed -->
	<!-- <div class="debug-info text-xs p-2 bg-accent/30 m-2 rounded">
		Current step: {$currentStep}, ServiceStatus: {$serviceStatus.status}
	</div> -->

	<div class="table">
		<div class="progress-bar-container">
			<div class="progress-info">
				<div class="text-sm font-medium">Progress</div>
				<div class="text-2xl font-bold">{$scanProgress}% scanned</div>
			</div>
			<Progress value={$scanProgress} max={100} class="w-[100%]" />
		</div>
		<!-- Force table to show loading animation when scan is in progress -->
	<Table 
		data={tableData} 
		columns={data.tableColumns} 
		currentStep={$currentStep} 
	/>
	</div>

	<div class="button-section">
		<div class="button-group">
			{#if $currentStep === 'running'}
				<Button
					onclick={() => scanPaused.set(!$scanPaused)}
					variant="default"
					size="default"
					class="pause-button"
				>
					{$scanPaused ? 'Resume' : 'Pause'}
				</Button>
				<Button
					onclick={() => (showStopDialog = true)}
					variant="destructive"
					size="default"
					class="stop-button"
				>
					Stop
				</Button>
			{:else}
				<Button onclick={handleRestart} variant="default" size="default" class="restart-button">
					Restart
				</Button>
				<Button onclick={handleRestart} variant="default" size="default" class="view-all-results">
					View All Results
				</Button>
			{/if}
		</div>
		<div class="single-button">
			<Button variant="secondary" size="default" class="terminal-button">Terminal</Button>
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
