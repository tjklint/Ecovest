<script lang="ts">
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';
    
    let symbols: string[] = [];
    let selectedSymbol = '';
    let environmentScore = 0;
    let socialScore = 0;
    let governanceScore = 0;
    let totalEsg = 0;
    let esgMap: Record<string, { environmentScore: number; socialScore: number; governanceScore: number; totalEsg: number }> = {};
    let bars: { label: string; score: number }[] = [];
    let pipelineText = '';
    let gicsSector = '';
    let gicsSubIndustry = '';
    let chartCanvas: HTMLCanvasElement;
    
    function getBarColor(score: number) {
      if (score <= 10) return '#22c55e';
      if (score <= 20) return '#eab308';
      return '#ef4444';
    }
    
    function getBarWidth(score: number) {
      const max = 30;
      const pct = (score / max) * 100;
      return Math.min(pct, 100);
    }
    
    function updateScores() {
      if (esgMap[selectedSymbol]) {
        environmentScore = esgMap[selectedSymbol].environmentScore;
        socialScore = esgMap[selectedSymbol].socialScore;
        governanceScore = esgMap[selectedSymbol].governanceScore;
        totalEsg = esgMap[selectedSymbol].totalEsg;
      } else {
        environmentScore = 0;
        socialScore = 0;
        governanceScore = 0;
        totalEsg = 0;
      }
    }
    
    async function fetchPipelineText(ticker) {
  try {
    let pipelineText = 'Loading...';
    let gicsSector = 'Loading...';
    const res = await fetch(`/api/pipeline/${ticker}`);
    if (!res.ok) throw new Error(`Error: ${res.status}`);
    const data = await res.json();

    // Extract text and GICS Sector
    const outputText = data.text;
    const outputData = data.data;

    if (outputText) {
      pipelineText = outputText;
    } else {
      pipelineText = 'No output available.';
    }

    if (outputData) {
      gicsSector = outputData['GICS Sector'];
      gicsSubIndustry = outputData['GICS Sub-Industry'];
    }

    console.log('Pipeline Text:', pipelineText);
    console.log('GICS Sector:', gicsSector);

    // Update the DOM with the new values
    document.getElementById('pipelineText').textContent = pipelineText;
    document.getElementById('gicsSector').textContent = gicsSector;
    document.getElementById('gicsSubIndustry').textContent = gicsSubIndustry;

  } catch (err) {
    pipelineText = 'Failed to fetch pipeline data.';
    console.error(err);
  }
}

  
    async function fetchPredictionData(ticker: string) {
      
      try {
        const res = await fetch(`/api/predict/${ticker}`);
        if (!res.ok) throw new Error(`Error: ${res.status}`);
        const data = await res.json();
        return data;
      } catch (err) {
        console.error("Failed to fetch prediction data:", err);
      }
    }

    let chartInstance: Chart | null = null;
    
    async function createChart(ticker) {
  try {
    console.log(`Fetching prediction data for ticker: ${ticker}`);

    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }

    renderPlaceholderChart(ticker);

    const predictionData = await fetchPredictionData(ticker);
    if (!predictionData) {
      console.error("No prediction data received.");
      return;
    }

    const historicalDates = predictionData.historical.dates;
    const historicalPrices = predictionData.historical.prices;

    const lastHistoricalDate = new Date(historicalDates[historicalDates.length - 1]);

    const futureDates = predictionData.predicted.dates.map((_, index) => {
      const futureDate = new Date(lastHistoricalDate);
      futureDate.setDate(lastHistoricalDate.getDate() + index + 1);
      return futureDate.toISOString().split('T')[0];
    });

    const mean = 0;
    const stdDev = 0.005;
    const gaussianRandom = () =>
      mean + stdDev * Math.sqrt(-2 * Math.log(Math.random())) * Math.cos(2 * Math.PI * Math.random());

    const smoothedPredictedPrices = predictionData.predicted.prices.map((price) => {
      const noise = gaussianRandom();
      return price * (1 + noise);
    });

    const combinedDates = historicalDates.concat(futureDates);
    const paddedHistoricalPrices = historicalPrices.concat(Array(futureDates.length).fill(null));
    const paddedPredictedPrices = Array(historicalDates.length).fill(null).concat(smoothedPredictedPrices);

    chartInstance.data.labels = combinedDates;
    chartInstance.data.datasets = [
      {
        label: "Historical Stock Prices",
        data: paddedHistoricalPrices,
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59, 130, 246, 0.2)",
        fill: false,
        pointRadius: 0,
        pointHoverRadius: 5,
      },
      {
        label: "Predicted Stock Prices",
        data: paddedPredictedPrices,
        borderColor: "#f97316",
        backgroundColor: "rgba(249, 115, 22, 0.2)",
        fill: false,
        pointRadius: 0,
        pointHoverRadius: 5,
      },
    ];

    chartInstance.options.plugins.title.text = `Stock Prices for ${ticker}`;
    chartInstance.update(); 

    console.log("Chart creation complete.");
  } catch (error) {
    console.error("Error during chart creation:", error);
    renderErrorChart(ticker); 
  }
}

function renderPlaceholderChart(ticker) {
  chartInstance = new Chart(chartCanvas, {
    type: "line",
    data: {
      labels: [], 
      datasets: [
        {
          label: "Loading Data...",
          data: [], 
          borderColor: "#ccc", 
          backgroundColor: "rgba(204, 204, 204, 0.2)",
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: `Loading Stock Prices for ${ticker}...`, 
          font: {
            size: 18,
            weight: "bold",
          },
        },
      },
      scales: {
        x: { type: "category" },
        y: { beginAtZero: true },
      },
    },
  });
}

function renderErrorChart(ticker) {
  chartInstance = new Chart(chartCanvas, {
    type: "line",
    data: {
      labels: [], 
      datasets: [
        {
          label: "Error Loading Data",
          data: [],
          borderColor: "#ff0000",
          backgroundColor: "rgba(255, 0, 0, 0.2)",
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: `Error Loading Stock Prices for ${ticker}`,
          font: {
            size: 18,
            weight: "bold",
          },
        },
      },
    },
  });
}
   async function handleSymbolChange() {
      updateScores();
      await fetchPipelineText(selectedSymbol);
      await createChart(selectedSymbol);
    }
  
    onMount(async () => {
      const res = await fetch('http://localhost:5173/data/sp500_esg_data.csv');
      const csv = await res.text();
      const lines = csv.trim().split('\n');
      const dataLines = lines.slice(1);
      dataLines.forEach((line) => {
        const cols = line.split(',');
        const symbol = cols[0];
        const e = parseFloat(cols[4]) || 0;
        const s = parseFloat(cols[5]) || 0;
        const g = parseFloat(cols[6]) || 0;
        const t = parseFloat(cols[7]) || 0;
        esgMap[symbol] = { environmentScore: e, socialScore: s, governanceScore: g, totalEsg: t };
      });
      symbols = Object.keys(esgMap);
      if (symbols.length > 0) {
        selectedSymbol = symbols[0];
        updateScores();
        await fetchPipelineText(selectedSymbol);
        await createChart(selectedSymbol);
      }
      bars = [
        { label: 'Environment', score: environmentScore },
        { label: 'Social', score: socialScore },
        { label: 'Governance', score: governanceScore },
        { label: 'Total ESG', score: totalEsg },
      ];
    });
  
    $: bars = [
      { label: 'Environment', score: environmentScore },
      { label: 'Social', score: socialScore },
      { label: 'Governance', score: governanceScore },
      { label: 'Total ESG', score: totalEsg },
    ];
  </script>
  
  <div class="container">
    <label for="stock-select" class="label">Select Ticker:</label>
    <select id="stock-select" bind:value={selectedSymbol} on:change={handleSymbolChange}>
      {#each symbols as symbol}
        <option value={symbol}>{symbol}</option>
      {/each}
    </select><div class="row" style="display: flex; align-items: stretch;">
      <div class="box chart-box" style="width: 70%;">
        <canvas bind:this={chartCanvas}></canvas>
      </div>
      <div class="box" style="width: 30%; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div class="header">Industry</div>
          <p id="gicsSector">{gicsSector || 'Fetching...'}</p>
        </div>
        <div>
          <div class="header">Sub-Industry</div>
          <p id="gicsSubIndustry">{gicsSubIndustry || 'Fetching...'}</p>
        </div>
      </div>
    </div>
    <div class="row" style="display: flex; align-items: stretch;">
      <div class="box" style="width: 60%;">
        <div class="header">ESG Score</div>
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
      <div class="box" style="width: 40%; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div class="header">Company Summary</div>
          <p id="pipelineText">{pipelineText || 'Fetching..'}</p>
        </div>
      </div>
    </div>
    
    
  </div>
  
  <style>
    .container {
      max-width: 1200px;
      margin: 3rem auto;
      padding: 0 2rem;
      font-family: 'Segoe UI', Roboto, sans-serif;
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
      height: 300px;
      box-sizing: border-box;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: flex-start;
      padding: 2rem;
      font-weight: 600;
      font-size: 1rem;
    }
    .box:not(:last-child) {
      margin-right: 1rem;
    }
    .header {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 1rem;
      width: 100%;
      text-align: left;
      color: #444;
    }
    .bars {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      margin-top: 0.5rem;
    }
    .bar-container {
      background-color: #f4f4f4;
      border-radius: 8px;
      overflow: hidden;
      width: 100%;
      height: 35px;
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
    .chart-box {
      height: 400px;
      align-items: stretch;
      justify-content: stretch;
      padding: 1rem;
    }
    .chart-box canvas {
      width: 100%;
      height: 100%;
    }
  </style>
  