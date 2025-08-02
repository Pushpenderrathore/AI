// script.js
async function sendPrompt() {
  const prompt = document.getElementById('prompt').value;

  try {
    const res = await fetch('https://ai-production-0bb3.up.railway.app/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ prompt })
    });

    if (!res.ok) {
      throw new Error(`Server error: ${res.status} ${res.statusText}`);
    }

    const data = await res.json();

    // Prefer response if available, fallback to error
    document.getElementById('responseBox').innerText = data.response || data.error || 'No response from AI.';
  } catch (err) {
    document.getElementById('responseBox').innerText = `Error: ${err.message}`;
  }
}

