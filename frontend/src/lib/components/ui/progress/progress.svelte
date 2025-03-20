<script>
	import { Progress as ProgressPrimitive } from 'bits-ui';
	import { cn } from '$lib/utils.js';

	let { ref = $bindable(null), class: className, max = 100, value, ...restProps } = $props();
</script>

<ProgressPrimitive.Root
	bind:ref
	class={cn('relative h-4 w-full overflow-hidden rounded-full bg-background1', className)}
	{value}
	{max}
	{...restProps}
>
	<div
		class="h-full w-full flex-1 bg-accent transition-all"
		style={`transform: translateX(-${100 - (100 * (value ?? 0)) / (max ?? 1)}%)`}
	></div>
</ProgressPrimitive.Root>
