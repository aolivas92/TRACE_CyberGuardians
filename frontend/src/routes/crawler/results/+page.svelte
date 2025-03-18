<script>
  export let data;
</script>

<h1>Crawler Results</h1>
<ul>
  {#each data.results as result}
    <li>{result.url} - {result.status}</li>
  {/each}
</ul>
