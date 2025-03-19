<script>
	import { cn } from "$lib/utils.js";

	let {
			ref = $bindable(null),
			value = $bindable(),
			type,
			files = $bindable(),
			class: className,
			...restProps
	} = $props();
</script>

{#if type === "file"}
	<input
			bind:this={ref}
			class={cn(
					"border-input bg-background ring-offset-background placeholder:text-background3 focus-visible:ring-accent3 flex h-10 w-full rounded-md border-1.5 px-3 py-2 text-base file:border-0 file:bg-transparent file:text-md file:font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-md",
					className
			)}
			type="file"
			bind:files
			bind:value
			{...restProps}
	/>
{:else if type === "number"}
	<input
			bind:this={ref}
			class={cn(
					"appearance-none no-spinner border-input bg-background ring-offset-background placeholder:text-background3 focus-visible:ring-accent3 flex h-10 w-full rounded-md border-1.5 px-3 py-2 text-base focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-md",
					className
			)}
			type="number"
			bind:value
			{...restProps}
	/>
{:else}
	<input
			bind:this={ref}
			class={cn(
					"border-input bg-background ring-offset-background placeholder:text-background3 focus-visible:ring-accent3 flex h-10 w-full rounded-md border-1.5 px-3 py-2 text-base focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-md",
					className
			)}
			{type}
			bind:value
			{...restProps}
	/>
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
