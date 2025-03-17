<script>
  import { Button } from "$lib/components/ui/button/index.js";
  import { Hammer, Network, FileCheck, Brain, Settings } from "lucide-svelte";
  import { toggleMode, mode} from "mode-watcher";
  let selectedIndex = null;

  function isSelected(index) {
    selectedIndex = selectedIndex === index ? null : index;
  }

  const menuItems = [
    { icon: Hammer, tooltip: "Tools" },
    { icon: Network, tooltip: "Network" },
    { icon: FileCheck, tooltip: "Results" },
    { icon: Brain, tooltip: "AI Model" },
  ];
</script>

<style>
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    width: 5rem;
    background-color: hsl(var(--background1));
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 1.3rem;
    border-radius: 0 0.9375rem 0.9375rem 0;
    box-shadow: rgba(13, 38, 76, 0.19) 0px 9px 20px;
  }

  .home-button {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 4rem;
  }

  .main-buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    flex-grow: 1;
    justify-content: center;
  }

  .settings-button {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 4rem;
  }
</style>

<div class="sidebar">
  <div class="home-button">
    <Button variant="link" size="icon" type="button" title="Toggle Theme">
      {#if mode === "dark"}
        <img src="/icons/traceDarkIcon.svg" alt="Dark Mode Icon" style="width: 2.6rem; height: 3;" />
      {:else}
        <img src="/icons/traceLightIcon.svg" alt="Light Mode Icon" style="width: 2.6rem; height: 3;" />
      {/if}
    </Button>
  </div>
  <div class="main-buttons">
    {#each menuItems as item, index}
      <Button
        variant="circle"
        size="circle"
        type="button"
        onclick={() => isSelected(index)}
        data-active={selectedIndex === index}
        title={item.tooltip} >
        <item.icon style="width: 1.5rem; height: 1.375rem;" />
      </Button>
    {/each}
  </div>
  <div class="settings-button">
    <Button onclick={toggleMode} variant="circle" size="circle" type="button" title="Settings">
      <Settings style="width: 1.5rem; height: 1.375rem;" />
    </Button>
  </div>
</div>
