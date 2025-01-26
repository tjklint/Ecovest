<script lang="ts">
  import { onMount } from "svelte";
  import Hero from "./lib/components/Hero.svelte";

  console.log(Hero); // Somehow necessary for Hero component to be registered

  let message = "Loading...";

  async function getMessage() {
    const res = await fetch("/api/hello");
    const data = await res.json();
    message = data.message;
  }
</script>

<main>
  <Hero />
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

</style>
