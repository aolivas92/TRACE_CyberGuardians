<script>
  import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from "$lib/components/ui/label/index.js";
	import { goto } from '$app/navigation';
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

	function handleInputChange(id, value) {
		formData[id] = value;
	}

	function handleSubmit() {
		console.log("Submitted Data:", formData);
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
          on:input={(e) => handleInputChange(field.id, e.target.value)}
        />
      </div>
    {/each}
		<div class="pt-5">
			<Button onclick={() => goto('/crawler/run')} variant="default" size="default" type="button" title="Submit" class="w-96">
				Submit
			</Button>
		</div>
  </div>
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