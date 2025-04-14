<script>
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import { Switch } from '$lib/components/ui/switch/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { goto } from '$app/navigation';
	import { validateField } from '$lib/validation/fieldValidatorFactory.js';
	import { enhance } from '$app/forms';
	import * as Tooltip from '$lib/components/ui/tooltip/index.js';
	import FormField from '$lib/components/ui/form/FormField.svelte';
	import { Info } from 'lucide-svelte';
	import { serviceStatus } from '$lib/stores/projectServiceStore';
	import { connectToCredGenAIWebSocket } from '$lib/services/credGenAISocket.js';

	let formData = {};
	let fieldErrors = {};
	let selectedFile = null;

	let usernameLength = '';
	let passwordLength = '';

	let inputFields = [
		{
			id: 'wordlist',
			label: 'Wordlist',
			type: 'file',
			required: true,
			toolTip: 'Upload a custom wordlist for generation (must be a .txt file).'
		},
		{
			id: 'username-length',
			label: 'Username Length',
			type: 'number',
			placeholder: '12',
			required: false
		},
		{
			id: 'password-length',
			label: 'Password Length',
			type: 'number',
			placeholder: '12',
			required: false
		}
	];

	let usernameToggles = [
		{ id: 'username-caps', label: 'Characters', checked: true },
		{ id: 'username-numbers', label: 'Numbers', checked: true },
		{ id: 'username-symbols', label: 'Symbols', checked: true }
	];

	let passwordToggles = [
		{ id: 'password-caps', label: 'Character', checked: true },
		{ id: 'password-numbers', label: 'Numbers', checked: true },
		{ id: 'password-symbols', label: 'Symbols', checked: true }
	];

	function toggleSwitch(category, index) {
		if (category === 'username') {
			usernameToggles[index].checked = !usernameToggles[index].checked;
		} else if (category === 'password') {
			passwordToggles[index].checked = !passwordToggles[index].checked;
		}
	}

	function handleInputChange(file) {
		selectedFile = file;
		const result = validateField('wordlist', file);
		fieldErrors.wordlist = result;
	}

	function handleLengthChange(id, value) {
		formData[id] = value;
		const result = validateField(id, value);
		fieldErrors[id] = result;
	}

	function validateAllFields() {
		let isValid = true;

		// Validate wordlist (file upload)
		const result = validateField('wordlist', selectedFile);
		fieldErrors['wordlist'] = result;

		if (result.error) {
			isValid = false;
		}

		return isValid;
	}

	const onSubmitHandler = () => {
		return async ({ result, update }) => {
			const isValid = validateAllFields();

			if (!isValid) {
				return;
			}

			if (result.type === 'success' && result.data?.success) {
				const jobId = result.data.job_id;

				if (!jobId) {
					console.error('Job ID missing from server response.');
					return;
				}

				// Save jobId to localStorage
				localStorage.setItem('currentCredGenAIJobId', jobId);

				// Delay connection slightly to let backend fully register job
				setTimeout(() => {
					import('$lib/services/credGenAISocket').then(({ connectToCredGenAIWebSocket }) => {
						console.log('[Form] Connecting to WebSocket for job:', jobId);
						connectToCredGenAIWebSocket(jobId);
					});
				}, 1000);

				// Go to results page
				goto('/credGenAI/results', { replaceState: true });
			} else {
				await update();
			}
		};
	};
</script>

<svelte:head>
	<title>CredGenAI Configuration | TRACE</title>
</svelte:head>

<div class="credGenAI-config">
	<div class="title-section">
		<div class="title">AI Generator</div>
		<StepIndicator status="config" />
	</div>

	<form
		method="POST"
		enctype="multipart/form-data"
		use:enhance={onSubmitHandler}
		class="input-container"
	>
		{#each inputFields.filter((f) => f.id === 'wordlist') as field}
			<FormField
				{field}
				value={formData[field.id] || ''}
				error={fieldErrors[field.id]?.error || false}
				errorText={fieldErrors[field.id]?.message || ''}
				onInput={(e) => handleInputChange(e.target.files?.[0] ?? null)}
				onBlur={() => handleInputChange(selectedFile)}
			/>
		{/each}

		<div class="toggle-container">
			<!-- Username Toggle Section -->
			<div class="toggle-section">
				<div class="flex items-center gap-2">
					<div class="toggle-title">Username</div>
					<Tooltip.Provider>
						<Tooltip.Root>
							<Tooltip.Trigger asChild>
								<Button
									variant="ghost"
									size="circlesm"
									type="button"
									aria-label="Information about username options"
								>
									<Info style="width: 16px; height: 16px;" />
								</Button>
							</Tooltip.Trigger>
							<Tooltip.Content>
								<p>All options are enabled by default</p>
							</Tooltip.Content>
						</Tooltip.Root>
					</Tooltip.Provider>
				</div>
				{#each usernameToggles as toggle, index}
					<div class="switch-container">
						<Label for={toggle.id}>{toggle.label}</Label>
						<fieldset class="toggle-section">
							<legend class="sr-only">Username generation options</legend>
							<Switch
								id={toggle.id}
								bind:checked={toggle.checked}
								oninput={() => toggleSwitch('username', index)}
							/>
							<input type="checkbox" class="sr-only" name={toggle.id} checked={toggle.checked} />
						</fieldset>
					</div>
				{/each}
				<div class="length-field">
					{#each inputFields.filter((f) => f.id === 'username-length') as field}
						<FormField
							{field}
							value={formData[field.id] || ''}
							error={fieldErrors[field.id]?.error || false}
							errorText={fieldErrors[field.id]?.message || ''}
							onInput={(e) => handleLengthChange(field.id, e.target.value)}
							onBlur={() => handleLengthChange(field.id, formData[field.id])}
						/>
					{/each}
				</div>
			</div>

			<!-- Password Toggle Section -->
			<div class="toggle-section">
				<div class="flex items-center gap-2">
					<div class="toggle-title">Password</div>
					<Tooltip.Provider>
						<Tooltip.Root>
							<Tooltip.Trigger asChild>
								<Button
									variant="ghost"
									size="circlesm"
									type="button"
									aria-label="Information about password options"
								>
									<Info style="width: 16px; height: 16px;" />
								</Button>
							</Tooltip.Trigger>
							<Tooltip.Content>
								<p>All options are enabled by default</p>
							</Tooltip.Content>
						</Tooltip.Root>
					</Tooltip.Provider>
				</div>
				{#each passwordToggles as toggle, index}
					<div class="switch-container">
						<Label for={toggle.id}>{toggle.label}</Label>
						<fieldset class="toggle-section">
							<legend class="sr-only">Password generation options</legend>
							<Switch
								id={toggle.id}
								bind:checked={toggle.checked}
								oninput={() => toggleSwitch('password', index)}
							/>
							<input type="checkbox" class="sr-only" name={toggle.id} checked={toggle.checked} />
						</fieldset>
					</div>
				{/each}
				<div class="length-field">
					{#each inputFields.filter((f) => f.id === 'password-length') as field}
						<FormField
							{field}
							value={formData[field.id] || ''}
							error={fieldErrors[field.id]?.error || false}
							errorText={fieldErrors[field.id]?.message || ''}
							onInput={(e) => handleLengthChange(field.id, e.target.value)}
							onBlur={() => handleLengthChange(field.id, formData[field.id])}
						/>
					{/each}
				</div>
			</div>
		</div>

		<div>
			<Button
				type="submit"
				variant="default"
				size="default"
				class="w-96"
				aria-label="Submit the form"
				title="Submit the form"
			>
				Submit
			</Button>
		</div>
	</form>
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
		font-size: 1.5rem;
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
	}
	.toggle-section {
		padding-top: 1rem;
		display: flex;
		flex-direction: column;
		width: 20%;
		height: 100%;
		gap: 1rem;
	}
	.toggle-title {
		font-size: 1.2rem;
		font-weight: bold;
		padding-bottom: 0.5rem;
	}
	.switch-container {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
	}
	.length-field {
		display: flex;
		flex-direction: column;
		padding-top: 1rem;
		height: 100%;
		min-height: 6.5rem;
		width: 100%;
	}
</style>
