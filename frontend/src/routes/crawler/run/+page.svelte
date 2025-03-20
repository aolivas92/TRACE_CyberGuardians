<script>
	import { Button } from '$lib/components/ui/button/index.js';
	import { goto } from '$app/navigation';
	import { Progress } from '$lib/components/ui/progress/index.js';
	import { onMount } from 'svelte';
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import Table from '$lib/components/ui/table/Table.svelte';
	import Alert from '$lib/components/ui/alert/Alert.svelte';

	//TODO: GET request to fetch data for the currentStep
	const { data } = $props();
	let value = $state(15);
	let currentStep = $state('running');
	let showStopDialog = $state(false);

	// Manage state
	onMount(() => {
		const interval = setInterval(() => {
			if (value < 100) {
				const randomIncrement = [3, 5, 10][Math.floor(Math.random() * 3)];
				value = Math.min(value + randomIncrement, 100);
			} else {
				clearInterval(interval);
				currentStep = 'results';
			}
		}, 500);
	});

	function handleStopCancel() {
		showStopDialog = false;
	}

	function handleStopConfirm() {
		showStopDialog = false;
		console.log('Crawler stopped');
		goto('/crawler/config');
	}
</script>

<div class="crawler-run">
	<div class="title-section">
		<div class="title">
			{currentStep === 'running' ? 'Crawler Scanning' : 'Crawler Results'}
		</div>
		<StepIndicator status={currentStep} />
	</div>

	<div class="table">
		<div class="progress-bar-container">
			<div class="progress-info">
				<div class="text-sm font-medium">Progress</div>
				<div class="text-2xl font-bold">{value}% scanned</div>
			</div>
			<Progress {value} max={100} class="w-[100%]" />
		</div>
		<Table data={data.tableData} columns={data.tableColumns} {currentStep} />
	</div>

	<!-- Button Section: Change buttons based on scan status -->
	<div class="button-section">
		<div class="button-group">
			{#if currentStep === 'running'}
				<Button
					onclick={() => goto('/crawler/config')}
					variant="default"
					size="default"
					class="restart-button"
				>
					Restart
				</Button>
				<Button
					onclick={() => goto('/crawler/run')}
					variant="default"
					size="default"
					class="pause-button"
				>
					Pause
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
				<!-- Change buttons when results are ready -->
				<Button
					onclick={() => goto('/crawler/config')}
					variant="default"
					size="default"
					class="restart-button"
				>
					Restart
				</Button>
				<!-- TODO: Redirect this to the Results page-->
				<Button
					onclick={() => goto('/crawler/config')}
					variant="default"
					size="default"
					class="view-all-results"
				>
					View All Results
				</Button>
			{/if}
		</div>
		<div class="single-button">
			<Button variant="secondary" size="default" class="terminal-button">Terminal</Button>
		</div>
	</div>

	<!-- Stop Confirmation Dialog -->
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
		padding: 0rem 3rem 3rem 3rem;
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
