// script.js
async function sendPrompt() {
  const prompt = document.getElementById('prompt').value;
  const responseDiv = document.getElementById('response');

  try {
    responseDiv.textContent = "Thinking...";

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
    responseDiv.textContent = data.response || "No response from AI.";
  } catch (err) {
    responseDiv.textContent = "Error: " + error.message;
  }
}

