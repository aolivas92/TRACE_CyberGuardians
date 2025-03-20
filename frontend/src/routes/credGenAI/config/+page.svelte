<script>
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import { Switch } from '$lib/components/ui/switch/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Button } from '$lib/components/ui/button/index.js';

	let currentStep = 'config';

	// Define toggle options for Username & Password
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

	// Function to toggle switch state
	function toggleSwitch(category, index) {
		if (category === 'username') {
			usernameToggles[index].checked = !usernameToggles[index].checked;
		} else if (category === 'password') {
			passwordToggles[index].checked = !passwordToggles[index].checked;
		}
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
			<Input id="wordlist" type="file" />
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
							on:change={() => toggleSwitch('username', index)}
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
							onchange={() => toggleSwitch('password', index)}
						/>
					</div>
				{/each}
			</div>
		</div>
		<Button variant="default" size="default" type="button" title="Submit" class="w-96">
			Submit
		</Button>
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
</style>
