<script lang="ts">
    import { onMount } from 'svelte'
    let symbols: string[] = []
    let selectedSymbol = ''
    let environmentScore = 0
    let socialScore = 0
    let governanceScore = 0
    let totalEsg = 0
    let esgMap: Record<string, { environmentScore: number; socialScore: number; governanceScore: number; totalEsg: number }> = {}
    
    function getBarColor(score: number) {
      if (score <= 10) return '#1ebd5c'
      if (score <= 20) return '#f1c40f'
      return '#e74c3c'
    }
    
    function getBarWidth(score: number) {
      const max = 30
      const pct = (score / max) * 100
      return Math.min(pct, 100)
    }
    
    function updateScores() {
      if (esgMap[selectedSymbol]) {
        environmentScore = esgMap[selectedSymbol].environmentScore
        socialScore = esgMap[selectedSymbol].socialScore
        governanceScore = esgMap[selectedSymbol].governanceScore
        totalEsg = esgMap[selectedSymbol].totalEsg
      } else {
        environmentScore = 0
        socialScore = 0
        governanceScore = 0
        totalEsg = 0
      }
    }
    
    function handleSymbolChange() {
      updateScores()
    }
    
    onMount(async () => {
      const res = await fetch('/data/sp500_esg_data.csv')
      const csv = await res.text()
      const lines = csv.trim().split('\n')
      const dataLines = lines.slice(1)
      dataLines.forEach(line => {
        const cols = line.split(',')
        const symbol = cols[0]
        const e = parseFloat(cols[4]) || 0
        const s = parseFloat(cols[5]) || 0
        const g = parseFloat(cols[6]) || 0
        const t = parseFloat(cols[7]) || 0
        esgMap[symbol] = { environmentScore: e, socialScore: s, governanceScore: g, totalEsg: t }
      })
      symbols = Object.keys(esgMap)
      if (symbols.length > 0) {
        selectedSymbol = symbols[0]
        updateScores()
      }
    })
    
    $: bars = [
      { label: 'Environment', score: environmentScore },
      { label: 'Social', score: socialScore },
      { label: 'Governance', score: governanceScore },
      { label: 'Total ESG', score: totalEsg }
    ]
    </script>
    
    <div class="container">
      <label for="stock-select" class="label">Select Ticker:</label>
      <select id="stock-select" bind:value={selectedSymbol} on:change={handleSymbolChange}>
        {#each symbols as symbol}
          <option value={symbol}>{symbol}</option>
        {/each}
      </select>
      <div class="row">
        <div class="box" style="width: 60%;">
          <div class="bars">
            {#each bars as bar}
              <div class="bar-container">
                <div
                  class="bar"
                  style="
                    width: {getBarWidth(bar.score)}%;
                    background-color: {getBarColor(bar.score)};
                  "
                >
                  {bar.label}: {bar.score}
                </div>
              </div>
            {/each}
          </div>
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
    .bars {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .bar-container {
      background-color: #f4f4f4;
      border-radius: 8px;
      overflow: hidden;
      width: 100%;
      height: 30px;
    }
    .bar {
      color: #fff;
      text-shadow: 1px 1px rgba(0, 0, 0, 0.4);
      font-size: 0.9rem;
      display: flex;
      align-items: center;
      height: 100%;
      padding-left: 0.5rem;
      border-radius: 8px 0 0 8px;
      transition: width 0.3s ease;
    }
    </style>
    