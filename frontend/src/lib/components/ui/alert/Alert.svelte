<script>
	// Props for the component
	export let isOpen = false;
	export let title = ' ';
	export let message = ' ';
	export let onCancel = () => {
		isOpen = false;
	};
	export let onContinue = () => {
		isOpen = false;
	};

	function handleBackdropClick(event) {
		if (event.target === event.currentTarget) {
			onCancel();
		}
	}

	function handleKeydown(event) {
		if (event.key === 'Escape') {
			onCancel();
		}
	}
</script>

<svelte:window on:keydown={handleKeydown} />

{#if isOpen}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
		role="button"
		tabindex="0"
		on:click={handleBackdropClick}
		on:keydown={(event) => event.key === 'Enter' && handleBackdropClick(event)}
	>
		<div
			class="mx-4 w-full max-w-md overflow-hidden rounded-lg bg-background shadow-lg"
			role="alertdialog"
			aria-modal="true"
			aria-labelledby="alert-title"
			aria-describedby="alert-message"
		>
			<div class="p-6">
				<h2 id="alert-title" class="mb-2 text-xl font-semibold text-foreground">{title}</h2>
				<p id="alert-message" class="mb-6 text-foreground">{message}</p>

				<div class="flex justify-end gap-3">
					<button
						class="rounded-md bg-accent px-4 py-2 text-background transition-colors hover:bg-accent1"
						on:click={onCancel}
					>
						Cancel
					</button>
					<button
						class="rounded-md bg-background1 px-4 py-2 text-foreground transition-colors hover:bg-background2"
						on:click={onContinue}
					>
						Continue
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
