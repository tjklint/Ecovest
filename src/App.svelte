<script lang="ts">
  import { onMount } from "svelte";
  import Hero from "./lib/components/Hero.svelte";

  let message = "Loading...";
  
  async function getMessage() {
    const res = await fetch("/api/hello");
    const data = await res.json();
    message = data.message;
  }

</script>

<main>
  <Hero tagline="Empowering sustainable investments" />

  <h1>My Svelte + Flask App</h1>
<p>{message}</p>
<button on:click={getMessage}>Refresh from Flask</button>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
  }
</style>