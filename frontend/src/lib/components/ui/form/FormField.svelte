<script>
  import { Input } from '$lib/components/ui/input/index.js';
  import { Label } from '$lib/components/ui/label/index.js';
  
  export let id;
  export let label;
  export let type = "text";
  export let placeholder = "";
  export let required = false;
  export let value = "";
  export let error = false;
  export let errorText = "";
  export let onInput;
  export let onBlur;
</script>

<div class="input-field">
  <Label for={id}>
    {label}
    {#if required}
      <span class="text-red-500">*</span>
    {/if}
  </Label>

  <Input
    {id}
    name={id}
    label={label}
    {type}
    {placeholder}
    {value}
    oninput={onInput}
    onblur={onBlur}
    {error}
    errorText={errorText}
  />
</div>

<style>
  .input-field {
    display: flex;
    width: 100%;
    max-width: 24rem;
    flex-direction: column;
    gap: 0.375rem;
  }
</style>