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
	let isSubmitting = false;
	let statusMessage = "";
	let targetUrlError = false;
	let targetUrlErrorText = "";

	function handleInputChange(id, value) {
		formData[id] = value;
		// Validate the target URL on input change
		if (id === "target-url") {
			validateTargetUrl();
		}
	}

	function validateTargetUrl() {
		const url = formData["target-url"];
		if (!url || url.trim() === "") {
			targetUrlError = true;
			targetUrlErrorText = "Target URL is required.";
		} else if (!/^https?:\/\/[^\s/$.?#].[^\s]*$/.test(url)) {
			targetUrlError = true;
			targetUrlErrorText = "Please enter a valid URL.";
		} else {
			targetUrlError = false;
			targetUrlErrorText = "";
		}
	}

	async function handleSubmit() {
		console.log("Form Data:", formData);

		// Validate before submission
		validateTargetUrl();
		if (targetUrlError) {
			statusMessage = "Please correct errors before submitting.";
			return false;
		}

		isSubmitting = true;
		statusMessage = "Sending data...";

		try {
			const response = await fetch("/crawler/config", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(formData),
			});

			console.log("Response status:", response.status);

			const result = await response.json();
			console.log("Response:", result);

			if (response.ok) {
				statusMessage = "Crawler started successfully!";
				return true; // Indicating success
			} else {
				statusMessage = `Error: ${result.message || "Unknown error"}`;
				return false; // Indicating failure
			}
		} catch (error) {
			statusMessage = "Failed to send data. Check console for details.";
			console.error("Error sending data:", error);
			return false; // Indicating failure
		} finally {
			isSubmitting = false;
		}
	}
</script>

<div class="crawler-config">
	<div class="title-section">
		<div class="title">Crawler Configuration</div>
		<StepIndicator status={currentStep} />
	</div>
	<div class="input-container">
		{#each inputFields as field}
			<div class="input-field">
				<Label for={field.id}>{field.label}</Label>
				{#if field.id === "target-url"}
					<Input
						id={field.id}
						type={field.type}
						placeholder={field.placeholder}
						bind:value={formData[field.id]}
						oninput={(e) => handleInputChange(field.id, e.target.value)}
						onblur={validateTargetUrl}
						error={targetUrlError}
						errorText={targetUrlErrorText}
					/>
				{:else}
					<Input
						id={field.id}
						type={field.type}
						placeholder={field.placeholder}
						bind:value={formData[field.id]}
						oninput={(e) => handleInputChange(field.id, e.target.value)}
					/>
				{/if}
			</div>
		{/each}
		<div class="pt-5">
			<Button
				onclick={async () => {
					const success = await handleSubmit();
					if (success) {
						goto('/crawler/run');
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