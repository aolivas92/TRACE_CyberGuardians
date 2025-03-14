<script>
	import { tv } from 'tailwind-variants';
	import * as Tooltip from '$lib/components/ui/tooltip/index.js';
	import { cn } from '$lib/utils.js';
	import { useSidebar } from './context.svelte.js';

	// Sidebar button styling variants
	export const sidebarMenuButtonVariants = tv({
		base: 'peer/menu-button ring-sidebar-ring hover:bg-sidebar-accent hover:text-sidebar-accent-foreground active:bg-sidebar-accent active:text-sidebar-accent-foreground data-[active=true]:bg-sidebar-accent data-[active=true]:text-sidebar-accent-foreground data-[state=open]:hover:bg-sidebar-accent data-[state=open]:hover:text-sidebar-accent-foreground flex w-full items-center gap-2 overflow-hidden rounded-md p-2 text-left text-sm outline-none transition-[width,height,padding] focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50 group-has-[[data-sidebar=menu-action]]/menu-item:pr-8 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active=true]:font-medium group-data-[collapsible=icon]:!size-8 group-data-[collapsible=icon]:!p-2 [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0',
		variants: {
			variant: {
				default: 'hover:bg-sidebar-accent hover:text-sidebar-accent-foreground',
				outline:
					'bg-background hover:bg-sidebar-accent hover:text-sidebar-accent-foreground shadow-[0_0_0_1px_hsl(var(--sidebar-border))] hover:shadow-[0_0_0_1px_hsl(var(--sidebar-accent))]'
			},
			size: {
				default: 'h-8 text-sm',
				sm: 'h-7 text-xs',
				lg: 'h-12 text-sm group-data-[collapsible=icon]:!p-0'
			}
		},
		defaultVariants: {
			variant: 'default',
			size: 'default'
		}
	});

	// Component Props (JavaScript style)
	export let ref = null;
	export let className = '';
	export let children;
	export let child;
	export let variant;
	export let size;
	export let isActive = false;
	export let tooltipContent;
	export let tooltipContentProps = {};
	export let restProps = {};

	// Sidebar state
	const sidebar = useSidebar();

	// Merging props
	const buttonProps = {
		class: cn(sidebarMenuButtonVariants({ variant, size }), className),
		'data-sidebar': 'menu-button',
		'data-size': size,
		'data-active': isActive,
		...restProps
	};
</script>

<!-- Render Button -->
{#if !tooltipContent}
	<button bind:this={ref} {...buttonProps}>
		{#if child}
			{child({ props: buttonProps })}
		{:else if children}
			{children()}
		{/if}
	</button>
{:else}
	<Tooltip.Root>
		<Tooltip.Trigger>
			<button bind:this={ref} {...buttonProps}>
				{#if child}
					{child({ props: buttonProps })}
				{:else if children}
					{children()}
				{/if}
			</button>
		</Tooltip.Trigger>
		<Tooltip.Content
			class=""
			side="right"
			align="center"
			hidden={sidebar.state !== 'collapsed' || sidebar.isMobile}
			{...tooltipContentProps}
		>
			{tooltipContent}
		</Tooltip.Content>
	</Tooltip.Root>
{/if}
