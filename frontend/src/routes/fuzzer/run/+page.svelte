<script>
	import { Button } from '$lib/components/ui/button/index.js';
	import { goto } from '$app/navigation';
	import { Progress } from '$lib/components/ui/progress/index.js';
	import { onMount } from 'svelte';
	import { serviceStatus } from '$lib/stores/projectServiceStore.js';
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import Table from '$lib/components/ui/table/Table.svelte';
	import Alert from '$lib/components/ui/alert/Alert.svelte';
	import { derived } from 'svelte/store';
	import { get } from 'svelte/store';
	import { onDestroy } from 'svelte';
	import { scanProgress, stopScanProgress, scanPaused } from '$lib/stores/scanProgressStore.js';

	const { data } = $props();
	let showStopDialog = $state(false);
	let paused = $state(false);

	const currentStep = derived(serviceStatus, ($serviceStatus) =>
		$serviceStatus.status === 'running'
			? 'running'
			: $serviceStatus.status === 'complete'
				? 'results'
				: 'config'
	);

	function handleStopCancel() {
		showStopDialog = false;
	}

	function handleStopConfirm() {
		showStopDialog = false;
		stopScanProgress();
		scanProgress.set(0);

		serviceStatus.set({
			status: 'idle',
			serviceType: 'fuzzer',
		});

		console.log('Fuzzer stopped');
		console.log('Current service status:', get(serviceStatus));
		goto('/dashboard');
	}

	function handleRestart() {
		stopScanProgress();
		scanProgress.set(0);

		console.log('Restarting at', new Date().toISOString());
		serviceStatus.set({
			status: 'idle',
			serviceType: null,
		});
		console.log('Current service status:', get(serviceStatus));
		goto('/fuzzer/config');
	}
</script>

<div class="fuzzer-run">
	<div class="title-section">
		<div class="title">
			{$currentStep === 'running' ? 'Fuzzer Scanning' : 'Fuzzer Results'}
		</div>
		<StepIndicator status={$currentStep} />
	</div>

	<div class="table">
		<div class="progress-bar-container">
			<div class="progress-info">
				<div class="text-sm font-medium">Progress</div>
				<div class="text-2xl font-bold">{$scanProgress}% scanned</div>
			</div>
			<Progress value={$scanProgress} max={100} class="w-[100%]" />
		</div>
		<Table data={data.tableData} columns={data.tableColumns} currentStep={$currentStep} />
	</div>

	<div class="button-section">
		<div class="button-group">
			{#if $currentStep === 'running'}
				<Button
					onclick={() => goto('/fuzzer/config')}
					variant="default"
					size="default"
					class="restart-button"
				>
					Restart
				</Button>
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
		message="This action cannot be undone. This will permanently stop the fuzzer and save current progress."
		onCancel={handleStopCancel}
		onContinue={handleStopConfirm}
	/>
</div>

<style>
	.fuzzer-run {
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
