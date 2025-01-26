<script lang="ts">
  import { onMount } from "svelte";
  import Hero from "./lib/components/Hero.svelte";
  import Navbar from './lib/components/Navbar.svelte';
  console.log(Hero); // Somehow necessary for Hero component to be registered
  console.log(Navbar); // Somehow necessary for Navbar component to be registered

  let message = "Loading...";

  async function getMessage() {
    const res = await fetch("/api/hello");
    const data = await res.json();
    message = data.message;
  }

  const navItems = [
    { name: 'Home', link: '/', icon: 'home' },
    { name: 'Chart', link: '/analytics', icon: 'chart' },
  ];
</script>

<main>
  <Navbar {navItems} />
  <Hero />
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

</style>
