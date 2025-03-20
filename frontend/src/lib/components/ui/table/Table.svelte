<script>
  import { Skeleton } from "$lib/components/ui/skeleton/index.js";
  export let data = [];
  export let columns = [];
  export let currentStep = "";
  
</script>
<div class="container flex flex-col items-center justify-center">
  <div class="table-body rounded-lg shadow-[0_8px_30px_rgb(0,0,0,0.12)]">
    <table class="w-full border-collapse">
      <thead class="sticky-header">
        <tr class="bg-accent text-background">
          {#each columns as column}
            <th class="p-2 text-left">{column.label}</th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#if currentStep === "running"}
          {#each Array(15) as _, i}
            <tr class={i % 2 === 0 ? 'bg-background1' : 'bg-background2'}>
              {#each columns as column}
                <td class="border-t p-2">
                  <Skeleton class="h-4 w-3/4 bg-background3" />
                </td>
              {/each}
            </tr>
          {/each}
        {:else}
          {#each data.slice(0, 15) as row, i}
            <tr class={i % 2 === 0 ? 'bg-background1' : 'bg-background2'}>
              {#each columns as column}
                <td class="border-t p-2">
                  {#if column.isLink}
                    <a href={row[column.key]} class="block max-w-xs truncate">{row[column.key]}</a>
                  {:else}
                    {row[column.key]}
                  {/if}
                </td>
              {/each}
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
</div>

<style>
  .container {
    width: 90%;
    max-width: 100%;
    padding: 4rem;
  }
  .table-body {
    max-height: 400px;
    max-width: 1200px;
    overflow-y: auto;
    width: 100%;
    display: flex;
    justify-content: center;
  }
  table {
    font-size: 14px;
    width: 100%;
    margin: auto;
    border-collapse: collapse;
  }
  .sticky-header {
    position: sticky;
    top: 0;
    background: var(--accent);
    z-index: 10;
  }
  th {
    font-weight: 700;
    text-align: left;
  }
  td {
    font-weight: 400;
  }
  @media (max-width: 768px) {
    .container {
      overflow-x: auto;
    }
  }
  ::-webkit-scrollbar {
    display: none;
  }
</style>