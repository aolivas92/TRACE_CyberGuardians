<script>
	import { cn } from '$lib/utils.js';

	let {
		ref = $bindable(null),
		value = $bindable(),
		type,
		files = $bindable(),
		class: className,
		error = false,
		errorText = '',
		...restProps
	} = $props();
</script>

{#if type === 'file'}
	<div class="w-full">
		<input
			bind:this={ref}
			class={cn(
				'no-spinner file:text-md md:text-md flex h-10 w-full rounded-md border-1.5 border-background3 border-input bg-background px-3 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:font-medium placeholder:text-background3 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent3-hover focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50',
				error && 'border-error focus-visible:ring-error-outline',
				className
			)}
			type="file"
			bind:files
			bind:value
			{...restProps}
		/>
		{#if error}
			<p class="mt-1 text-sm text-error">{errorText}</p>
		{/if}
	</div>
{:else}
	<div class="w-full">
		<input
			bind:this={ref}
			class={cn(
				'no-spinner md:text-md flex h-10 w-full rounded-md border-1.5 border-background3 border-input bg-background px-3 py-2 text-base ring-offset-background placeholder:text-background3 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent3-hover focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50',
				error && 'border-error focus-visible:ring-error-outline',
				className
			)}
			{type}
			bind:value
			{...restProps}
		/>
		{#if error}
			<p class="mt-1 text-sm text-error">{errorText}</p>
		{/if}
	</div>
{/if}

<style>
	.no-spinner {
		-moz-appearance: textfield;
	}
	.no-spinner::-webkit-inner-spin-button,
	.no-spinner::-webkit-outer-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
</style>
