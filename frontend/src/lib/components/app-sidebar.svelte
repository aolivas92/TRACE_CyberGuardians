<script lang="ts">
  import { Hammer, Network, Settings, } from "lucide-svelte";

  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  
  // Menu items.
  const items = [
   {
    title: "Services",
    url: "#",
    icon: Hammer,
   },
   {
    title: "TreeGraph",
    url: "#",
    icon: Network,
   },
   {
    title: "Settings",
    url: "#",
    icon: Settings,
   },
  ];
 </script>
  
 <Sidebar.Root class="app-sidebar">
  <Sidebar.Content class="">
   <Sidebar.Group class="group">
    <Sidebar.GroupLabel class="group-label" child="application">Application</Sidebar.GroupLabel>
    <Sidebar.GroupContent class="group-content">
     <Sidebar.Menu class="menu">
      {#each items as item (item.title)}
      <Sidebar.MenuItem class="menu-item">
        <Sidebar.MenuButton
          size="default"
          child={item.title}
          variant="default"
          tooltipContent={item.title}
        >
          <a href={item.url} class="">
            <item.icon />
            <span>{item.title}</span>
          </a>
        </Sidebar.MenuButton>
      </Sidebar.MenuItem>
      {/each}
     </Sidebar.Menu>
    </Sidebar.GroupContent>
   </Sidebar.Group>
  </Sidebar.Content>
 </Sidebar.Root>