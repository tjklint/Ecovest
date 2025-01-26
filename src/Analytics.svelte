<script lang="ts">
    let stocks = ["AAPL", "BBB", "GME"];
    let selectedStock: string = stocks[0];
  </script>
  
  <div class="container">
    <label for="stock-select" class="label">Choose a stock:</label>
    <select id="stock-select" bind:value={selectedStock}>
      {#each stocks as stock}
        <option value={stock}>{stock}</option>
      {/each}
    </select>
  
    <!-- Row 1 -->
    <div class="row">
      <!-- 60% width box -->
      <div class="box" style="width: 60%;">
        Rectangle 1
      </div>
      <!-- 40% width box -->
      <div class="box" style="width: 40%;">
        Rectangle 2
      </div>
    </div>
  
    <!-- Row 2 -->
    <div class="row">
      <!-- 70% width box -->
      <div class="box" style="width: 70%;">
        Rectangle 3
      </div>
      <!-- 30% width box -->
      <div class="box" style="width: 30%;">
        Rectangle 4
      </div>
    </div>
  </div>
  
  <style>
    .container {
      max-width: 1200px;
      margin: 3rem auto;
      padding: 0 2rem;
      font-family: "Segoe UI", Roboto, sans-serif;
    }
  
    .label {
      display: inline-block;
      margin-bottom: 0.5rem;
      font-weight: 500;
      font-size: 1.1rem;
    }
  
    select {
      display: block;
      margin-bottom: 2rem;
      padding: 0.6rem 1rem;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 1rem;
      outline: none;
      cursor: pointer;
      transition: box-shadow 0.2s ease-in-out;
    }
    select:focus {
      box-shadow: 0 0 3px rgba(66, 153, 225, 0.6);
    }
  
    .row {
      display: flex;
      margin-bottom: 2rem;
    }
  
    .box {
      border: 1px solid #ddd;
      border-radius: 8px;
      background: #fefefe;
      height: 200px; 
      box-sizing: border-box;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem; 
      font-weight: 600;
      font-size: 1rem;
    }
  
    .box:not(:last-child) {
      margin-right: 1rem;
    }
    .container {
      max-width: 1200px;
      margin: 3rem auto;
      padding: 0 2rem;
      font-family: "Segoe UI", Roboto, sans-serif;
    }
  
    .label {
      display: inline-block;
      margin-bottom: 0.5rem;
      font-weight: 500;
      font-size: 1.1rem;
    }
  
    select {
      display: block;
      margin-bottom: 2rem;
      padding: 0.6rem 1rem;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 1rem;
      outline: none;
      cursor: pointer;
      transition: box-shadow 0.2s ease-in-out;
    }
    select:focus {
      box-shadow: 0 0 3px rgba(66, 153, 225, 0.6);
    }
  
    /* Each row is flex to lay out boxes horizontally */
    .row {
      display: flex;
      margin-bottom: 2rem; /* more space between rows */
    }
  
    /* Each rectangle box: bigger, with shadow, radius, etc. */
    .box {
      border: 1px solid #ddd;
      border-radius: 8px;
      background: #fefefe;
      /* Increase size for a bigger wireframe area */
      height: 200px; 
      box-sizing: border-box;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
      display: flex;
      align-items: center;  /* vertically center content */
      justify-content: center; /* horizontally center content */
      padding: 2rem; 
      font-weight: 600;
      font-size: 1rem;
      /* optional: letter-spacing, text-transform, etc. */
    }
  
    /* Space between boxes in a row */
    .box:not(:last-child) {
      margin-right: 1rem;
    }
  </style>
  