<script lang="ts">
    export let tagline = "Invest in a sustainable future";
  </script>
  
  <section class="hero">
    <div class="hero-content">
      <h1 class="hero-title">Ecovest</h1>
      <p class="hero-tagline">{tagline}</p>
    </div>
  </section>
  
  <style>
    .hero {
      display: flex;
      align-items: center;
      justify-content: flex-start;
      background-color: #f0f0f0;
      height: 100vh;
    }
    .hero-content {
      margin-left: 2rem;
    }
    .hero-title {
      font-size: 4rem;
      font-weight: bold;
      margin-bottom: 0.5rem;
    }
    .hero-tagline {
      font-size: 1.5rem;
      color: #666;
    }
  </style>