<script>
    let prompt = '';
    let response = '';
  
    const API_KEY = "sAAA";
  
    async function getResponse() {
      try {
        const res = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${API_KEY}`
          },
          body: JSON.stringify({
            model: 'gpt-3.5-turbo',
            messages: [
              { role: 'user', content: prompt }
            ]
          })
        });
  
        if (!res.ok) {
          throw new Error(`OpenAI API error: ${res.status} ${res.statusText}`);
        }
  
        const data = await res.json();
        if (data && data.choices && data.choices.length > 0) {
          response = data.choices[0].message.content;
        } else {
          response = "No response received.";
        }
      } catch (err) {
        console.error(err);
      }
    }
  </script>
  
  <main>
    <h1>ChatGPT in Svelte</h1>
    <input type="text" bind:value={prompt} placeholder="Enter your prompt" />
    <button on:click={getResponse}>Ask ChatGPT</button>
    <p>{response}</p>
  </main>
  