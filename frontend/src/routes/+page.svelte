<script>
  import { Button } from "$lib/components/ui/button/index.js";  
  import { toggleMode } from "mode-watcher";

</script>

<div class="container">
  <div class="title">Theme switch</div>
  <Button onclick={toggleMode} variant="default" class="" size="default" type="button">Button</Button>
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center; 
    justify-content: center;
    height: 100vh;
    gap: 1rem;
  }

  .title {
    font-size: 2rem;
    font-weight: 600;
    text-align: center;
  }
</style>