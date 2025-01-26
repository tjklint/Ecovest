<script lang="ts">
  import Hero from "./lib/components/Hero.svelte";
  import GeminiApi from "./lib/components/Insights.svelte";
</script>

<main>
  <Hero tagline="Empowering sustainable investments" />
  <GeminiApi />
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
  }
</style>