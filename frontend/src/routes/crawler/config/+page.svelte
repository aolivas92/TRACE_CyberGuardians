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

	let formData = {};
	let fieldErrors = {};

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
			id: 'depth',
			label: 'Crawl Depth',
			type: 'number',
			placeholder: '5',
			required: false,
			advanced: false
		},
		{
			id: 'excluded-urls',
			label: 'Excluded URLs',
			type: 'text',
			placeholder: 'Comma-separated URLs to skip',
			required: false,
			advanced: true
		},
		{
			id: 'crawl-date',
			label: 'Crawl Date',
			type: 'date',
			required: false,
			advanced: false
		},
		{
			id: 'crawl-time',
			label: 'Crawl Time',
			type: 'time',
			required: false,
			advanced: false
		},
		{
			id: 'max-pages',
			label: 'Max Pages',
			type: 'number',
			placeholder: '50',
			required: false,
			advanced: true
		},
		{
			id: 'user-agent',
			label: 'User Agent',
			type: 'text',
			placeholder: 'https://juice-shop.herokuapp.com/drink/*',
			required: false,
			advanced: true
		},
		{
			id: 'delay',
			label: 'Request Delay',
			type: 'number',
			placeholder: '1000',
			required: false,
			advanced: true
		},
		{
			id: 'proxy',
			label: 'Proxy',
			type: 'number',
			placeholder: '8080',
			required: false,
			advanced: true
		}
	];

	function handleInputChange(id, value) {
		formData[id] = value;
		const result = validateField(id, value);
		fieldErrors[id] = result;
	}

	function validateAllFields() {
		let isValid = true;

		inputFields.forEach((field) => {
			const result = validateField(field.id, formData[field.id]);
			fieldErrors[field.id] = result;

			if (field.required && (!formData[field.id] || result.error)) {
				isValid = false;
			}
		});

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
					serviceType: 'crawler',
					startTime: new Date()
				});

				startScanProgress(); 

				goto('/crawler/run', { replaceState: true });
			} else {
				await update();
			}
		};
	};

	$: console.log('[CURRENT STATUS]', $serviceStatus);
$: console.log('[CURRENT PROGRESS]', $scanProgress);

</script>

<div class="crawler-config">
	<div class="title-section">
		<div class="title">Crawler Configuration</div>
		<StepIndicator status="config" />
	</div>
	<form method="POST" use:enhance={onSubmitHandler} class="input-container">
		{#each inputFields.filter((field) => !field.advanced) as field}
		{#if field.id === 'target-url'}
			<div class="w-full max-w-96 flex flex-col">
				<div class="flex items-center input-field">
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
	.crawler-config {
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
