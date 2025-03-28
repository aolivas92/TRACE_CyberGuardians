<script>
	import { enhance } from '$app/forms';
	import { onMount } from 'svelte';
	// import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';

	let formData = {};
	let targetUrlError = false;
	let targetUrlErrorText = '';

	let inputFields = [
		{
			id: 'target-url',
			label: 'Target URL',
			type: 'text',
			placeholder: 'https://juice-shop.herokuapp.com',
			required: true
		},
		{ id: 'depth', label: 'Crawl Depth', type: 'number', placeholder: '2' },
		{ id: 'max-pages', label: 'Max Pages', type: 'number', placeholder: '50' },
		{
			id: 'user-agent',
			label: 'User Agent',
			type: 'text',
			placeholder: 'https://juice-shop.herokuapp.com/drink/*'
		},
		{ id: 'delay', label: 'Request Delay', type: 'number', placeholder: '1000' },
		{ id: 'proxy', label: 'Proxy', type: 'number', placeholder: '8080' }
	];

	function handleInputChange(id, value) {
		formData[id] = value;
		if (id === 'target-url') {
			validateTargetUrl();
		}
	}

	function validateTargetUrl() {
		const url = formData['target-url'];
		if (!url || url.trim() === '') {
			targetUrlError = true;
			targetUrlErrorText = 'Target URL is required.';
		} else if (!/^https?:\/\/[^\s/$.?#].[^\s]*$/.test(url)) {
			targetUrlError = true;
			targetUrlErrorText = 'Please enter a valid URL.';
		} else {
			targetUrlError = false;
			targetUrlErrorText = '';
		}
	}

	const onSubmitHandler = ({ result }) => {
		if (result.type === 'success' && result.data?.success) {
			console.log('✅ All good!');
		}
	};
</script>

<div class="crawler-config">
	<div class="title-section">
		<div class="title">Crawler Configuration</div>
		<StepIndicator status="config" />
	</div>

	<form method="POST"
	use:enhance={{ onSubmit: onSubmitHandler }}
	class="input-container">
		{#each inputFields as field}
			<div class="input-field">
				<Label for={field.id}>
					{field.label}
					{#if field.required}
						<span class="text-red-500">*</span>
					{/if}
				</Label>

				{#if field.id === 'target-url'}
					<div class="flex flex-row">
						<Input
							id={field.id}
							type={field.type}
							placeholder={field.placeholder}
							value={formData[field.id] ?? ''}
							oninput={(e) => handleInputChange(field.id, e.target.value)}
							onblur={validateTargetUrl}
							error={targetUrlError}
							errorText={targetUrlErrorText}
						/>

						<Tooltip.TooltipProvider>
							<Tooltip.Root>
								<Tooltip.Trigger>i</Tooltip.Trigger>
								<Tooltip.Content>
									<p>
										Only Target URL is required.
										<br />
										The rest will use default values if left blank.
									</p>
								</Tooltip.Content>
							</Tooltip.Root>
						</Tooltip.TooltipProvider>
					</div>
				{:else}
					<Input
						id={field.id}
						type={field.type}
						placeholder={field.placeholder}
						oninput={(e) => handleInputChange(field.id, e.target.value)}
					/>
				{/if}
			</div>
		{/each}

		<div class="pt-5">
			<!-- <Button type="submit" variant="default" size="default" class="w-96">
				dfgdfgdfgdfgdf
			</Button> -->
			<button type="submit">Submit</button>

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
		margin-bottom: 8rem;
		max-width: 100%;
		height: 100%;
		gap: 1rem;
	}
	.input-field {
		display: flex;
		width: 100%;
		max-width: 24rem;
		flex-direction: column;
		gap: 0.375rem;
	}
</style>
