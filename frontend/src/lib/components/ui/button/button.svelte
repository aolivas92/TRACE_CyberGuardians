<script module>
	import { tv } from "tailwind-variants";

	export const buttonVariants = tv({
		base: "ring-offset-background focus-visible:ring-ring inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
		variants: {
			variant: {
				default: "bg-accent text-accent-foreground hover:bg-accent/80",
				destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
				outline: "border-input bg-background hover:bg-accent hover:text-accent-foreground border",
				secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
				ghost: "hover:bg-accent hover:text-accent-foreground",
				link: "text-primary underline-offset-4 hover:underline",
				circle: "bg-background2 text-background2-foreground hover:bg-accent hover:text-accent-foreground rounded-full drop-shadow-md data-[active=true]:bg-accent data-[active=true]:bg-accent data-[active=true]:text-accent-foreground"
			},
			size: {
				default: "h-10 px-4 py-2 rounded-lg",
				sm: "h-9 px-3 rounded-lg",
				lg: "h-11 px-8 rounded-lg",
				icon: "h-10 w-10",
				circle: "h-11 w-11",
			},
		},
		defaultVariants: {
			variant: "default",
			size: "default",
		},
	});
</script>

<script>
	import { cn } from "$lib/utils.js";

	let {
		class: className,
		variant,
		size,
		ref = $bindable(null),
		href = undefined,
		type,
		children,
		...restProps
	} = $props();
</script>

{#if href}
	<a bind:this={ref} class={cn(buttonVariants({ variant, size }), className)} {href} {...restProps}>
		{@render children?.()}
	</a>
{:else}
	<button
		bind:this={ref}
		class={cn(buttonVariants({ variant, size }), className)}
		{type}
		{...restProps}
	>
		{@render children?.()}
	</button>
{/if}
