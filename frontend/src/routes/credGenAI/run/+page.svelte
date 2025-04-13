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
		console.log('AI Generator stopped');
		goto('/credGenAI/config');
	}

	function handleExportWordList() {
	try {
		const headers = data.tableColumns.map(col => col.label);
		const csvRows = [
			headers.join(','),
			...data.tableData.map(row =>
				headers.map(h => JSON.stringify(row[h.replace(/\s/g, '')] || '')).join(',')
			)
		];

		const csvContent = csvRows.join('\n');
		const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = 'credGenAI_wordlist.csv';
		document.body.appendChild(a);
		a.click();
		a.remove();
		window.URL.revokeObjectURL(url);
	} catch (err) {
		alert('Failed to export word list');
		console.error(err);
	}
}

</script>

<svelte:head>
  <title>CredGenAI Run | TRACE</title>
</svelte:head>

<div class="generator-run">
	<div class="title-section">
		<div class="title">
			{currentStep === 'running' ? 'AI Generator Running' : 'AI Generator Results'}
		</div>
		<StepIndicator status={currentStep} />
	</div>

	<div class="table">
		<div class="progress-bar-container">
			<div class="progress-info">
				<div class="text-sm font-medium">Progress</div>
				<div class="text-2xl font-bold">{value}% generated</div>
			</div>
			<Progress {value} max={100} class="w-[100%]" />
		</div>
		<Table data={data.tableData} columns={data.tableColumns} {currentStep} />
	</div>

	<div class="button-section">
		{#if currentStep === 'running'}
			<Button
				onclick={() => (showStopDialog = true)}
				variant="destructive"
				size="default"
				class="stop-button"
				aria-label="Cancel the process"
				title="Cancel the process"
			>
				Cancel
			</Button>
		{:else}
			<div class="button-group">
				<Button
					onclick={() => goto('/credGenAI/config')}
					variant="secondary"
					size="default"
					class="restart-button"
					aria-label="Re-generate the configuration"
					title="Re-generate the configuration"
				>
					Re-Generate
				</Button>
				<Button
					onclick={handleExportWordList}
					variant="default"
					size="default"
					class="save-button"
					aria-label="Save the word list"
					title="Save the word list"
				>
					Save
				</Button>
			</div>
		{/if}
	</div>

	<Alert
		isOpen={showStopDialog}
		title="Are you absolutely sure?"
		message="This action will stop the current process. You won't be able to undo this action."
		onCancel={handleStopCancel}
		onContinue={handleStopConfirm}
	/>
</div>

<style>
	.generator-run {
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
		width: 100%;
		justify-content: end;
		padding: 0rem 8rem 3rem 3rem;
	}
	.button-group {
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
