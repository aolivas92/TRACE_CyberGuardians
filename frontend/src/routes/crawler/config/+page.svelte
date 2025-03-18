<script>
  let url = "";
</script>

<h1>Configure Crawler</h1>
<input bind:value={url} placeholder="Enter target URL" />
<button on:click={() => console.log("Start crawler for", url)}>Start</button>
