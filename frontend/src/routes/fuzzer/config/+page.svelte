<script>
	import { enhance, applyAction } from '$app/forms';
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { validateField } from '$lib/validation/validationRules';
	import { goto } from '$app/navigation';
	import { serviceStatus } from '$lib/stores/projectServiceStore';
	import { Info } from 'lucide-svelte';
	import { scanProgress, startScanProgress } from '$lib/stores/scanProgressStore.js';
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import FormField from '$lib/components/ui/form/FormField.svelte';
	import * as Accordion from '$lib/components/ui/accordion/index.js';
	import * as Tooltip from '$lib/components/ui/tooltip/index.js';
	import * as RadioGroup from '$lib/components/ui/radio-group/index.js';

	let formData = {};
	let fieldErrors = {};
	let selectedFile = null;
	let httpMethod = 'GET';

	let inputFields = [
		{
			id: 'target-url',
			label: 'Target URL',
			type: 'text',
			placeholder: 'https://juice-shop.herokuapp.com',
			required: true,
			advanced: false
		},
		{
			id: 'parameters',
			label: 'Parameters (username, password, etc.)',
			type: 'text',
			placeholder: 'username, password',
			required: true,
			advanced: false
		},
		{
			id: 'headers',
			label: 'Headers',
			type: 'text',
			placeholder: 'User-Agent: Mozilla/5.0',
			required: false,
			advanced: true
		},
		{
			id: 'proxy',
			label: 'Proxy URL',
			type: 'text',
			placeholder: 'http://127.0.0.1:8080',
			required: false,
			advanced: true
		},
		{
			id: 'body-template',
			label: 'Body Template (POST Body)',
			type: 'text',
			placeholder: 'username: payload, password: payload',
			required: false,
			advanced: true
		}
	];

	function handleInputChange(id, value) {
		if (id === 'wordlist') {
			selectedFile = value;
			fieldErrors.wordlist = validateField('wordlist', selectedFile);
		} else {
			formData[id] = value;
			const fieldResult = validateField(id, value);
			fieldErrors[id] = fieldResult;
		}
	}

	function validateAllFields() {
		let isValid = true;

		inputFields.forEach((field) => {
			const value = formData[field.id];
			const result = validateField(field.id, value);
			fieldErrors[field.id] = result;

			if (field.required && (!value || result.error)) {
				isValid = false;
			}
		});

		// Validate the wordlist file
		const fileResult = validateField('wordlist', selectedFile);
		fieldErrors.wordlist = fileResult;

		if (fileResult.error) {
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
				scanProgress.set(0);

				serviceStatus.set({
					status: 'running',
					serviceType: 'fuzzer',
					startTime: new Date()
				});

				startScanProgress();

				goto('/fuzzer/run', { replaceState: true });
			} else {
				await update();
			}
		};
	};
</script>

<div class="fuzzer-config">
	<div class="title-section">
		<div class="title">Fuzzer Configuration</div>
		<StepIndicator status="config" />
	</div>
	<form
		method="POST"
		enctype="multipart/form-data"
		use:enhance={onSubmitHandler}
		class="input-container"
	>
		{#each inputFields.filter((field) => !field.advanced) as field}
			{#if field.id === 'target-url'}
				<div class="flex w-full max-w-96 flex-col">
					<div class="input-field flex items-center">
						<Label for={field.id} class="font-medium">
							{field.label}
							{#if field.required}
								<span class="text-red-500">*</span>
							{/if}
						</Label>
						<Tooltip.Provider>
							<Tooltip.Root>
								<Tooltip.Trigger asChild>
									<Button variant="ghost" size="circlesm" type="button">
										<Info style="width: 16px; height: 16px;" />
									</Button>
								</Tooltip.Trigger>
								<Tooltip.Content>
									<p>Optional fields left empty will use default values</p>
								</Tooltip.Content>
							</Tooltip.Root>
						</Tooltip.Provider>
					</div>
					<FormField
						id={field.id}
						type={field.type}
						placeholder={field.placeholder}
						value={formData[field.id] || ''}
						error={fieldErrors[field.id]?.error || false}
						errorText={fieldErrors[field.id]?.message || ''}
						onInput={(e) => handleInputChange(field.id, e.target.value)}
						onBlur={() => handleInputChange(field.id, formData[field.id])}
					/>
				</div>
			{:else}
				<FormField
					id={field.id}
					label={field.label}
					type={field.type}
					placeholder={field.placeholder}
					required={field.required}
					value={formData[field.id] || ''}
					error={fieldErrors[field.id]?.error || false}
					errorText={fieldErrors[field.id]?.message || ''}
					onInput={(e) => handleInputChange(field.id, e.target.value)}
					onBlur={() => handleInputChange(field.id, formData[field.id])}
				/>
				<FormField
					id="wordlist"
					label="Wordlist"
					type="file"
					required={true}
					error={fieldErrors.wordlist?.error || false}
					errorText={fieldErrors.wordlist?.message || ''}
					onInput={(e) => handleInputChange('wordlist', e.target.files?.[0] ?? null)}
					onBlur={() => handleInputChange('wordlist', selectedFile)}
					class="w-full rounded border px-3 py-2"
				/>

				<Label for="HTTP-method" class="flex w-full max-w-96 gap-1 font-medium">
					HTTP Method
					{#if field.required}
						<span class="text-red-500">*</span>
					{/if}
				</Label>
				<RadioGroup.Root bind:value={httpMethod} class="flex w-full max-w-96 flex-row gap-4">
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="GET" id="get" />
						<Label for="get">GET</Label>
					</div>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="PUT" id="put" />
						<Label for="put">PUT</Label>
					</div>
					<div class="flex items-center space-x-2">
						<RadioGroup.Item value="POST" id="post" />
						<Label for="post">POST</Label>
					</div>
				</RadioGroup.Root>
				<!-- Hidden input to send the HTTP method to the server -->	
				<input type="hidden" name="http-method" value={httpMethod} />
			{/if}
		{/each}

		<Accordion.Root type="single" class="w-96 max-w-full">
			<Accordion.Item value="item-1">
				<Accordion.Trigger>Advanced Settings</Accordion.Trigger>
				<Accordion.Content>
					{#each inputFields.filter((field) => field.advanced) as field}
						<FormField
							id={field.id}
							label={field.label}
							type={field.type}
							placeholder={field.placeholder}
							required={field.required}
							value={formData[field.id] || ''}
							error={fieldErrors[field.id]?.error || false}
							errorText={fieldErrors[field.id]?.message || ''}
							onInput={(e) => handleInputChange(field.id, e.target.value)}
							onBlur={() => handleInputChange(field.id, formData[field.id])}
						/>
					{/each}
				</Accordion.Content>
			</Accordion.Item>
		</Accordion.Root>

		<div class="pb-8">
			<Button type="submit" variant="default" size="default" class="w-96">Submit</Button>
		</div>
	</form>
</div>

<style>
	.fuzzer-config {
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
		max-width: 100%;
		height: 100%;
		gap: 1rem;
	}
	.input-field {
		display: flex;
		width: 100%;
		max-width: 24rem;
		flex-direction: row;
		gap: 0.375rem;
	}
</style>
