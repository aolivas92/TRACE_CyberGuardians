<script>
	import { goto } from '$app/navigation';
	import { Button } from '$lib/components/ui/button/index.js';
	export let data;
</script>

<div class="dashboard">
	<div class="title-section">
		<div class="title">Dashboard</div>
		<div class="proj-name">{data.projectName}</div>
	</div>

	<div class="cards-container">
		{#each data.tools as tool}
			<div class="card">
				<div class="tool-name">{tool.name}</div>
				<div class="tool-actions">
					<div class="tool-status">Status: {tool.status}</div>
					<Button
						variant="secondary"
						size="lg"
						data-active={tool.status === 'Started'}
						class={tool.status === 'Started' ? 'px-10' : ''}
						onclick={() => goto(tool.route)}
					>
						{tool.status === 'Not Started' ? 'Set Up' : 'View'}
					</Button>
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.dashboard {
		display: flex;
		margin-left: 4.5rem;
		height: 100vh;
		flex-direction: column;
	}

	.title-section {
		display: flex;
		flex-direction: column;
		max-height: fit-content;
		padding-bottom: 2rem;
	}

	.title {
		font-size: 2rem;
		font-style: normal;
		font-weight: 600;
		padding-left: 3rem;
		padding-top: 3rem;
	}

	.proj-name {
		font-size: 1.2rem;
		font-style: normal;
		font-weight: 600;
		padding-left: 3rem;
		padding-top: 0.5rem;
		color: var(--foreground);
	}

	.cards-container {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		padding-left: 3rem;
		padding-right: 3rem;
		max-width: 100%;
		gap: 2rem;
	}

	.card {
		border-radius: 0.6rem;
		width: 100%;
		background-color: var(--background1);
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		padding: 1rem 2.5rem 1rem 2.5rem;
	}

	.tool-name {
		font-size: 1.1rem;
		font-style: normal;
		font-weight: 500;
	}

	.tool-actions {
		display: flex;
		align-items: center;
		gap: 2rem;
	}

	.tool-status {
		font-size: 1rem;
		font-style: normal;
		font-weight: 400;
		color: var(--foreground);
	}
</style>
