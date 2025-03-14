<script>
	import '../app.css';
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  import AppSidebar from "$lib/components/app-sidebar.svelte";
	
	let { children } = $props();
</script>

<Sidebar.Provider class="" style="">
  <AppSidebar />
  <main>
    <Sidebar.Trigger class="trigger-class" onclick={() => {}} />
    {@render children?.()}
  </main>
</Sidebar.Provider>