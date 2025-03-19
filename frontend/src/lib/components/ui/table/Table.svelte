<script>
  export let data = [];
</script>

<div class="container">
  <table class="w-full border-collapse rounded-lg overflow-hidden shadow-[0_8px_30px_rgb(0,0,0,0.12)]">
    <thead>
      <tr class="bg-accent text-background"> 
        <th class="p-2 text-left">ID</th>
        <th class="p-2 text-left">URL</th>
        <th class="p-2 text-left">Title</th>
        <th class="p-2 text-left">Word Count</th>
        <th class="p-2 text-left">Character Count</th>
        <th class="p-2 text-left">Links Found</th>
        <th class="p-2 text-left">Error</th>
      </tr>
    </thead>
    <tbody>
      {#each data as row, i}
        <tr class={i % 2 === 0 ? 'bg-background1' : 'bg-background2'}>
          <td class="p-2 border-t">{row.id}</td>
          <td class="p-2 border-t">
            <a href={row.url} class="truncate block max-w-xs">{row.url}</a>
          </td>
          <td class="p-2 border-t">{row.title}</td>
          <td class="p-2 border-t">{row.wordCount}</td>
          <td class="p-2 border-t">{row.charCount}</td>
          <td class="p-2 border-t">{row.linksFound}</td>
          <td class="p-2 border-t">{row.error ? 'True' : 'False'}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<style>
  .container {
    width: 90%;
    max-width: 100%;
    padding: 4rem;
  }
  table {
    font-size: 14px;
  }
  
  th {
    font-weight: 700;
  }

  td {
    font-weight: 400;
  }

  @media (max-width: 768px) {
    .container {
      overflow-x: auto;
    }
  }
</style>
