<script>
  let progress = 0;

  function startScan() {
    const interval = setInterval(() => {
      progress += 10;
      if (progress >= 100) clearInterval(interval);
    }, 1000);
  }
</script>

<h1>Crawler Running...</h1>
<progress value={progress} max="100"></progress>
<button on:click={startScan}>Start Scan</button>
