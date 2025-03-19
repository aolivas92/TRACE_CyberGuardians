<script>
    import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from "$lib/components/ui/label/index.js";
	import StepIndicator from "$lib/components/ui/progressStep/ProgressStep.svelte";

	let inputFields = [
    { id: "target-url", label: "Target URL", type: "text", placeholder: "https://juice-shop.herokuapp.com" },
    { id: "depth", label: "Crawl Depth", type: "number", placeholder: "2" },
    { id: "max-pages", label: "Max Pages", type: "number", placeholder: "50" },
    { id: "user-agent", label: "User Agent", type: "text", placeholder: "https://juice-shop.herokuapp.com/drink/*" },
    { id: "delay", label: "Request Delay", type: "number", placeholder: "1000" },
    { id: "proxy", label: "Proxy", type: "number", placeholder: "8080" }
  ];

	let formData = {};
	let currentStep = "config"; 
	let isSubmitting = false;
	let statusMessage = "";

	function handleInputChange(id, value) {
		formData[id] = value;
	}

  async function handleSubmit() {
	console.log("Form Data:", formData);
      
	if (!formData["target-url"]) {
	statusMessage = "Target URL is required";
	return;
	}

	isSubmitting = true;
	statusMessage = "Sending data...";

	
    try {
      const response = await fetch("/crawler/config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

	  console.log("Response status:", response.status);

      const result = await response.json();
      console.log("Response:", result);

      if (response.ok) {
		statusMessage = "Crawler started successfully!";
      } else {
		statusMessage = `Error: ${result.message || "Unkown error"}`;
      }
    } catch (error) {
		statusMessage = "Failed to send data. Check console for"
      console.error("Error sending data:", error);
    } finally {
		isSubmitting = false;
	}
  }
</script>

<div class="crawler-config">
  <div class="title-section">
    <div class="title">Crawler Configuration</div>
		<StepIndicator status={currentStep}/>
  </div>
  <div class="input-container">
		{#each inputFields as field}
      <div class="input-field">
        <Label for={field.id}>{field.label}</Label>
        <Input 
          id={field.id} 
          type={field.type} 
          placeholder={field.placeholder} 
		  value={formData[field.id] || ''}
          oninput={(e) => handleInputChange(field.id, e.target.value)}
        />
      </div>
    {/each}
		<div class="pt-5">
			<Button onclick={handleSubmit} variant="defaultSec" size="default" type="button" title="Submit" class="w-96">
				Submit
			</Button>
		</div>
	{#if statusMessage}
	<div class="status-message {statusMessage.includes('Error') ? 'error' : 'success'}">
		{statusMessage}
	</div>
	{/if}
  </div>
</div>

<style>
	.crawler-config {
		display: flex;
		margin-left: 4.5rem;
		height: 100vh;
		flex-direction: column;
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