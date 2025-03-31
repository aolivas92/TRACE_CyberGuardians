<script>
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import { Switch } from '$lib/components/ui/switch/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { goto } from '$app/navigation';
	import { validateField } from '$lib/validation/validationRules.js';
	import { enhance } from '$app/forms';
	import FormField from '$lib/components/ui/form/FormField.svelte';

	let formData = {};
	let fieldErrors = {}; 
	let selectedFile = null;

	let usernameLength = "";
	let passwordLength = "";



	let inputFields = [
		{
		id: 'wordlist',
		label: 'Wordlist',
		type: 'file',
		required: true,
		
		},
	]

	let usernameToggles = [
		{ id: 'username-caps', label: 'Caps', checked: true },
		{ id: 'username-numbers', label: 'Numbers', checked: true },
		{ id: 'username-symbols', label: 'Symbols', checked: true }
	];

	let passwordToggles = [
		{ id: 'password-caps', label: 'Caps', checked: true },
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

	function handleInputChange(id, value) {
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
				goto('/credGenAI/run', { replaceState: true });
			} else {
				await update();
			}
		};
	};

		
</script>

<div class="credGenAI-config">
	<div class="title-section">
		<div class="title">AI Generator</div>
		<StepIndicator status = 'config' />
	</div>

	<form method="POST" enctype="multipart/form-data" use:enhance={onSubmitHandler} class="input-container">
		{#each inputFields.filter((field) => !field.advanced) as field}
			<FormField
				id={field.id}
				label={field.label}
				type={field.type}
				placeholder={field.placeholder}
				required={field.required}
				value={formData[field.id] || ''}
				error={fieldErrors[field.id]?.error || false}
				errorText={fieldErrors[field.id]?.message || ''}
				onInput={(e) => {
					if (field.type === 'file') {
						selectedFile = e.target.files?.[0] ?? null;
						handleInputChange(field.id, e.target.files?.[0] ?? null);
					} else {
						handleInputChange(field.id, e.target.value);
					}
				}}
				onBlur={() => handleInputChange(field.id, formData[field.id])}
			/>
		{/each}


		<div class="toggle-container">
			<!-- Username Toggle Section -->
			<div class="toggle-section">
				<div class="toggle-title">Username</div>
				<p class="text-sm italic text-gray-500">Note: Characters are always included.</p>
				{#each usernameToggles as toggle, index}
					<div class="switch-container">
						<Label for={toggle.id}>{toggle.label}</Label>
						<Switch
							id={toggle.id}
							bind:checked={toggle.checked}
							oninput={() => toggleSwitch('username', index)}
						/>
					</div>
				{/each}

				<div class="length-field">
					<Label for="username-length">Length</Label>
					<Input
						id="username-length"
						type="number"
						min="1"
						bind:value={usernameLength}
						placeholder='12'
						class="w-32"
					/>
				</div>
			</div>


			<!-- Password Toggle Section -->
			<div class="toggle-section">
				<div class="toggle-title">Password</div>
				<p class="text-sm italic text-gray-500">Note: Characters are always included.</p>
				{#each passwordToggles as toggle, index}
					<div class="switch-container">
						<Label for={toggle.id}>{toggle.label}</Label>
						<Switch
							id={toggle.id}
							bind:checked={toggle.checked}
							oninput={() => toggleSwitch('password', index)}
						/>
					</div>
				{/each}
				<div class="length-field">
					<Label for="password-length">Length</Label>
					<Input
						id="password-length"
						type="number"
						min="1"
						bind:value={passwordLength}
						placeholder='12'
						class="w-32"
					/>
				</div>
			</div>
		</div>

		<div>
			<Button type="submit" variant="default" size="default" class="w-96">Submit</Button>
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
		justify-content: space-between;
		align-items: center;
		width: 10rem;
	}
	.length-field {
	display: flex;
	flex-direction: column;;
	gap: 0.25rem;
	margin-top: 1rem;
}

</style>