// script.js
const cloudflareApi = "https://rugby-hc-flashers-her.trycloudflare.com/ask";
const localApi = "http://localhost:8080/ask";

async function sendPrompt() {
  const prompt = document.getElementById('prompt').value;
  const responseDiv = document.getElementById('response');
  const payload = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt })
  };

  responseDiv.textContent = "Thinking...";

  try {
    // Try Cloudflare URL first
    const res = await fetch(cloudflareApi, payload);
    if (!res.ok) throw new Error(`Cloudflare error: ${res.status} ${res.statusText}`);
    const data = await res.json();
    responseDiv.textContent = data.response || "No response from AI.";
  } catch (err1) {
    console.warn("Cloudflare failed, trying localhost...", err1.message);
    try {
      // Fallback to localhost
      const res = await fetch(localApi, payload);
      if (!res.ok) throw new Error(`Localhost error: ${res.status} ${res.statusText}`);
      const data = await res.json();
      responseDiv.textContent = data.response || "No response from AI.";
    } catch (err2) {
      console.error("Both endpoints failed:", err2);
      responseDiv.textContent = "Error: " + err2.message;
    }
  }
}


// // script.js
// const apiUrl = "https://rugby-hc-flashers-her.trycloudflare.com/ask";

// async function sendPrompt() {
//   const prompt = document.getElementById('prompt').value;
//   const responseDiv = document.getElementById('response');

//   try {
//     responseDiv.textContent = "Thinking...";

//     const res = await fetch('https://rugby-hc-flashers-her.trycloudflare.com/ask', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({ prompt })
//     });

//     if (!res.ok) {
//       const errorText = await res.text();  // sometimes server returns HTML/plain
//       throw new Error(`Server error: ${res.status} ${res.statusText}`);
//     }

//     const data = await res.json();
//     responseDiv.textContent = data.response || "No response from AI.";
//   } catch (err) {
//     console.error(err);
//     responseDiv.textContent = "Error: " + err.message;
//   }
// }

