<script>
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import { Switch } from '$lib/components/ui/switch/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { goto } from '$app/navigation';

	let currentStep = 'config';
	let selectedFile = null;
	let wordlistError = false;
	let wordlistErrorText = "";
	let isSubmitting = false;
	let statusMessage = "";

	let usernameToggles = [
		{ id: 'username-characters', label: 'Characters', checked: false },
		{ id: 'username-numbers', label: 'Numbers', checked: true },
		{ id: 'username-symbols', label: 'Symbols', checked: true }
	];

	let passwordToggles = [
		{ id: 'password-characters', label: 'Characters', checked: true },
		{ id: 'password-numbers', label: 'Numbers', checked: false },
		{ id: 'password-symbols', label: 'Symbols', checked: false }
	];

	function toggleSwitch(category, index) {
		if (category === 'username') {
			usernameToggles[index].checked = !usernameToggles[index].checked;
		} else if (category === 'password') {
			passwordToggles[index].checked = !passwordToggles[index].checked;
		}
	}

	function handleFileChange(event) {
		selectedFile = event.target.files[0];
		validateWordlist();
	}

	function validateWordlist() {
		if (!selectedFile) {
			wordlistError = true;
			wordlistErrorText = "Wordlist file is required.";
		} else {
			wordlistError = false;
			wordlistErrorText = "";
		}
	}

	async function handleSubmit() {
		validateWordlist();
		if (wordlistError) {
		statusMessage = "Please upload a wordlist file before submitting.";
		return false;
		}

		// Simulate success without actually sending anything
		statusMessage = "Pretending to upload wordlist...";
		await new Promise((resolve) => setTimeout(resolve, 500)); // fake delay

		return true;
	}
</script>

<div class="credGenAI-config">
	<div class="title-section">
		<div class="title">AI Generator</div>
		<StepIndicator status={currentStep} />
	</div>

	<div class="input-container">
		<div class="input-section">
			<Label for="wordlist">Wordlist</Label>
			<Input
				id="wordlist"
				type="file"
				onChange={handleFileChange}
				class="w-full border rounded px-3 py-2"
			/>
			{#if wordlistError}
				<p class="text-red-600 text-sm mt-1">{wordlistErrorText}</p>
			{/if}
		</div>

		<div class="toggle-container">
			<!-- Username Toggle Section -->
			<div class="toggle-section">
				<div class="toggle-title">Username</div>
				{#each usernameToggles as toggle, index}
					<div class="switch-container">
						<Label for={toggle.id}>{toggle.label}</Label>
						<Switch
							id={toggle.id}
							bind:checked={toggle.checked}
							onChange={() => toggleSwitch('username', index)}
						/>
					</div>
				{/each}
			</div>

			<!-- Password Toggle Section -->
			<div class="toggle-section">
				<div class="toggle-title">Password</div>
				{#each passwordToggles as toggle, index}
					<div class="switch-container">
						<Label for={toggle.id}>{toggle.label}</Label>
						<Switch
							id={toggle.id}
							bind:checked={toggle.checked}
							onChange={() => toggleSwitch('password', index)}
						/>
					</div>
				{/each}
			</div>
		</div>

		<div class="button-container">
			<Button
				onclick={async () => {
					const success = await handleSubmit();
					if (success) {
						goto('/credGenAI/run');
					}
				}}
				variant="default"
				size="default"
				type="button"
				title="Submit"
				class="w-96"
			>
				Submit
			</Button>
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
	.toggle-container {
		display: flex;
		flex-direction: row;
		justify-content: center;
		align-items: center;
		width: 100%;
		gap: 7rem;
		padding-bottom: 1rem;
	}
	.toggle-section {
		margin-top: 1rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
	.toggle-title {
		font-size: 1.2rem;
		font-weight: bold;
		margin-bottom: 0.5rem;
	}
	.switch-container {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}
	.input-section {
		display: flex;
		flex-direction: column;
		padding-bottom: 2rem;
		gap: 0.5rem;
	}
	.button-container {
		margin-top: 1rem;
	}
</style>