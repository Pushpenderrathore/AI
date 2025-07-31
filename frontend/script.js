async function sendPrompt() {
  const prompt = document.getElementById('prompt').value;
  const res = await fetch('https://<your-railway-app>.up.railway.app/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt })
  });

  const data = await res.json();
  document.getElementById('responseBox').innerText = data.response;
}
