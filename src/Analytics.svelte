<script lang="ts">
    import { onMount } from 'svelte';
  
    let symbols: string[] = [];
    let selectedStock: string = '';
  
    function handleSymbolChange() {

      console.log("Selected stock:", selectedStock);
    }
  
    onMount(async () => {
      const response = await fetch('/data/sp500_esg_data.csv');
      const csvText = await response.text();
      const lines = csvText.trim().split('\n');

      const dataLines = lines.slice(1);
      symbols = dataLines.map(line => line.split(',')[0]).filter(Boolean);
      if (symbols.length > 0) {
        selectedStock = symbols[0];
      }
    });
  </script>
  
  <div class="container">
    <label for="stock-select" class="label">Select Ticker:</label>
    <select id="stock-select" bind:value={selectedStock} on:change={handleSymbolChange}>
      {#each symbols as symbol}
        <option value={symbol}>{symbol}</option>
      {/each}
    </select>
  
    <div class="row">
      <div class="box" style="width: 60%;">
        Rectangle 1
      </div>
      <div class="box" style="width: 40%;">
        Rectangle 2
      </div>
    </div>
  
    <div class="row">
      <div class="box" style="width: 70%;">
        Rectangle 3
      </div>
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
  </style>
  