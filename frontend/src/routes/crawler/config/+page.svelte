<script>
	import { enhance, applyAction } from '$app/forms';
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	// import * as Tooltip from '$lib/components/ui/tooltip';
	import StepIndicator from '$lib/components/ui/progressStep/ProgressStep.svelte';
	import FormField from '$lib/components/ui/form/FormField.svelte';
	import { validateField } from '$lib/validation/validationRules';
	import { goto } from '$app/navigation';
  
  let formData = {};
  let fieldErrors = {};
  
  // Field definitions
	let inputFields = [
		{
			id: 'target-url',
			label: 'Target URL',
			type: 'text',
			placeholder: 'https://juice-shop.herokuapp.com',
			required: true
		},
		{
			id: 'depth',
			label: 'Crawl Depth',
			type: 'number',
			placeholder: '5',
			required: false
		},
		{
			id: 'excluded-urls',
			label: 'Excluded URLs',
			type: 'text',
			placeholder: 'Comma-separated URLs to skip',
			required: false
		},
		{
			id: 'crawl-date',
			label: 'Crawl Date',
			type: 'date',
			required: false
		},
		{
			id: 'crawl-time',
			label: 'Crawl Time',
			type: 'time',
			required: false
		},
		{
			id: 'max-pages',
			label: 'Max Pages',
			type: 'number',
			placeholder: '50',
			required: false
		},
		{
			id: 'user-agent',
			label: 'User Agent',
			type: 'text',
			placeholder: 'https://juice-shop.herokuapp.com/drink/*',
			required: false
		},
		{
			id: 'delay',
			label: 'Request Delay',
			type: 'number',
			placeholder: '1000',
			required: false
		},
		{
			id: 'proxy',
			label: 'Proxy',
			type: 'number',
			placeholder: '8080',
			required: false
		}
	];
  
  function handleInputChange(id, value) {
    formData[id] = value;
    const result = validateField(id, value);
    fieldErrors[id] = result;
  }
  
  function validateAllFields() {
    let isValid = true;
    
    inputFields.forEach(field => {
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
        goto('/crawler/run', { replaceState: true });
      } else {
        await update();
      }
    };
  };
</script>

<div class="crawler-config">
  <div class="title-section">
    <div class="title">Crawler Configuration</div>
    <StepIndicator status="config" />
  </div>

  <form method="POST" use:enhance={onSubmitHandler} class="input-container">
    {#each inputFields as field}
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

    <div class="pt-5">
      <Button type="submit" variant="default" size="default" class="w-96">
        Submit
      </Button>
    </div>
  </form>

		<!-- <Tooltip.TooltipProvider>
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
						</Tooltip.TooltipProvider> -->
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
</style>
