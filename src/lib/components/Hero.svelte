<script lang="ts">
  export let tagline = "Invest sustainably and responsibly.";
</script>

<section class="hero">
  <div class="grid-container">
    <div class="hero-content">
      <h1 class="hero-title">Ecovest</h1>
      <p class="hero-tagline">{tagline}</p>
      <div class="button-grid">
        <button class="ecovest-button" on:click={() => window.location.href = '/analytics'}>
          Analytics
        </button>
        <button class="github-button" on:click={() => window.open('https://github.com/tjklint/Ecovest', '_blank')}>
          GitHub
        </button>
      </div>
    </div>
    <div class="hero-sidebar">
      <p>Add complementary content here, like an image, stats, or additional info.</p>
    </div>
  </div>
</section>

<style>
.hero {
  width: 100%;
  display: flex;
  align-items: center;
  background-color: #f4f4f9;
  height: 100vh;
  margin-left: 2rem;
  padding: 0 0rem;
}

.grid-container {
  display: grid;
  grid-template-columns: 80% 20%;
  align-items: center;
  width: 100%;
  max-width: 1400px;
  margin: 0;
  gap: 1rem;
  height: 100%;
}

.hero-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-title {
  font-size: 7rem;
  font-weight: bold;
  margin: 0 0;
  margin-bottom: -0.5rem;
}

.hero-tagline {
  margin-top: 0;
  font-size: 2rem;
  color: #666;
}

.button-grid {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.ecovest-button {
  background-color: #96D291;
  color: #333333;
  border: none;
  border-radius: 12px;
  padding: 10px 32px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.ecovest-button:hover {
  background-color: #7EBA72;
}

.github-button {
  background-color: #a1989828;
  color: #333333;
  border: solid 2px #3333335f;
  border-radius: 12px;
  padding: 10px 34px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.github-button:hover {
  background-color: #867d7d42;
}

.hero-sidebar {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e8e8ef;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: 100%;
  }

  .hero-content {
    margin-bottom: 2rem;
  }

  .button-grid {
    flex-direction: column;
    gap: 0.8rem;
  }

  .hero-sidebar {
    margin-top: 1rem;
  }
}
</style>
