<script lang="ts">
    export let tagline = "Invest in a sustainable future";
  </script>
  
  <section class="hero">
    <div class="hero-content">
      <h1 class="hero-title">Ecovest</h1>
      <p class="hero-tagline">{tagline}</p>
      <div class="button-grid">
        <button class="ecovest-button" on:click={() => window.location.href = '/analytics'}>
          Ecovest <span class="arrow">{'>>'}</span>
        </button>
        <button class="github-button">
          GitHub
        </button>
      </div>
    </div>
  </section>
  
  <style>
    .hero {
      display: flex;
      align-items: center;
      justify-content: flex-start;
      background-color: #f0f0f0;
      height: 100vh;
      padding-left: 2rem;
      padding-right: 2rem;
      margin-top: -3rem;
      background-color: #f4f4f9;
    }
    .hero-content {
      margin-left: 2rem;
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

    
  .ecovest-button {
    background-color: #96D291;
    color: #333333;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 1em;
    display: flex;
    gap: 8px;
    cursor: pointer;
    font-size: 1.2rem;
  }

  .arrow {
    font-weight: 500;
    margin-top: 1px;
  }

  .ecovest-button:hover {
    background-color: #7EBA72;
  }

  .button-grid {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }

  .github-button {
    background-color: #a1989828;
    color: #333333;
    border: solid 2px #3333335f;
    border-radius: 12px;
    padding: 10px 32px;
    font-size: 1em;
    cursor: pointer;
    font-size: 1.2rem;
  }
  </style>