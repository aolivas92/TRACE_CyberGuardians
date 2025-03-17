<script>
  let tools = [
    { name: "Crawler", progress: "0%", route: "/crawler/config" }
  ];
</script>

<h1 class="text-2xl font-bold">Tool Dashboard</h1>

<ul>
  {#each tools as tool}
    <li>
      <a href={tool.route} class="block p-4 bg-gray-200 rounded-md mt-2">
        {tool.name} - {tool.progress}
      </a>
    </li>
  {/each}
</ul>
