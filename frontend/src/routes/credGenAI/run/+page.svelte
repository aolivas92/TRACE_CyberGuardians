<script>
	import { Button } from '$lib/components/ui/button/index.js';
	import { goto } from '$app/navigation';
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import Table from '$lib/components/ui/table/Table.svelte';

	export let data;

	let currentStep = 'results';

	// Load metadata from server
	let runningTime = data.runningTime;
	let usernamesGenerated = data.usernamesGenerated;
	let passwordsGenerated = data.passwordsGenerated;

	function handleReGenerate() {
		goto('/credGenAI/config'); 
	}

	function handleSaveWordList() {
		alert('Mock: Word list saved!');
	}
</script>

<div class="generator-run">
	<div class="title-section">
		<div class="title">AI Generator</div>
		
	</div>

	<div class="metrics">
		<div><strong>Running Time</strong><br />{runningTime}</div>
		<div><strong>Generated Usernames</strong><br />{usernamesGenerated}</div>
		<div><strong>Generated Passwords</strong><br />{passwordsGenerated}</div>
	</div>

	<Table data={data.tableData} columns={data.tableColumns} currentStep={currentStep} />

	<div class="button-section">
		<!-- Left side -->
		<div class="button-left">
			<Button
			onClick={() => {
				console.log("🔁 Re-Generate button clicked");
				goto('/credGenAI/config');
			}}
		>
			Re-Generate
		</Button>
		</div>
	
		<!-- Right side -->
		<div class="button-right">
			<Button onClick={handleSaveWordList} variant="secondary">Save Word List</Button>
		</div>
	</div>
</div>

<style>
	.generator-run {
		display: flex;
		flex-direction: column;
		padding: 3rem;
		margin-left: 4.5rem;
		gap: 2rem;
	}

	.title-section {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		padding-right: 3rem;
	}

	.title {
		font-size: 2rem;
		font-weight: 600;
	}

	.metrics {
		display: flex;
		justify-content: center;
		gap: 4rem;
		text-align: center;
		font-size: 1.05rem;
		padding-top: 1rem;
	}

	.button-section {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding-left: 3rem;
	padding-right: 3rem;
	margin-top: 1rem;
	}

	.button-left,
	.button-right {
		display: flex;
	}
</style>