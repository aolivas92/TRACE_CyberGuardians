<script>
	import StepIndicator from "$lib/components/ui/progressStep/ProgressStep.svelte";
	// import { Switch } from "$lib/components/ui/switch/index.js";
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from "$lib/components/ui/label/index.js";
	// import { Button } from '$lib/components/ui/button/index.js';

	let currentStep = "config";
</script>

<div class="credGenAI-config">
	<div class="title-section">
		<div class="title">AI Generator</div>
		<StepIndicator status={currentStep} />
	</div>
	<div class="input-container">
		<div>
			<Label for="model">Wordlist</Label>
			<Input id="wordlist" type="file" />
			<div class="">

			</div>
		</div>
	</div>
</div>

<style>
	.credGenAI-config {
		display: flex;
		margin-left: 4.5rem;
		height: 100vh;
		flex-direction: column;
		justify-content: space-around;
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
	.input-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding-left: 3rem;
		padding-right: 3rem;
		margin-bottom: 8rem;
		max-width: 100%;
		height: 100%;
		gap: 1rem;
	}
</style>
