<script>
  import Sidebar from "$lib/components/ui/sidebar/Sidebar.svelte";
  import { ModeWatcher } from "mode-watcher";
  import "../app.css";
</script>

<ModeWatcher />

<div class="app-container">
  <Sidebar />
  <main class="content">
    <slot />
  </main>
</div>

<style>
  .app-container {
    display: flex;
    height: 100vh;
  }

  .content {
    flex-grow: 1;
    overflow-y: auto;
		padding-left: 80px;
  }
</style>
