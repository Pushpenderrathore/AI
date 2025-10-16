import os
import sys
import requests
import socket
import threading
import datetime

# =============== CONFIGURATION ==================
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com/chat/completions"
model = "gpt-4.1"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

# =============== CORE MODEL FUNCTION ===============
def ask_model(prompt, history=None):
    """Send a prompt + optional history to the model"""
    messages = [{"role": "system", "content": "You are a helpful assistant for analyzing firewall alerts."}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    data = {
        "messages": messages,
        "model": model,
        "temperature": 0.7
    }

    resp = requests.post(endpoint, headers=headers, json=data)
    resp.raise_for_status()

    response_json = resp.json()
    return response_json["choices"][0]["message"]["content"]

# =============== LOCAL CHAT MODE ===============
def chat_mode():
    """Interactive chat session"""
    print("🤖 CyberGuard Chat Mode (type 'exit' or 'quit' to leave)")
    history = []
    while True:
        user_input = input(">>> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break
        try:
            answer = ask_model(user_input, history)
            print(f"gpt: {answer}\n")
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": answer})
        except Exception as e:
            print(f"⚠️ Error: {e}")

# =============== ALERT RESPONSE MODE ===============
def response():
    """Reads /var/log/alert.txt and sends its content to the model"""
    file_path = "/var/log/alert.txt"
    if not os.path.exists(file_path):
        print(f"⚠️ {file_path} not found. Run 'cyberwall | grep ALERT > alert.txt' first.")
        return
    
    with open(file_path, "r") as f:
        alerts = f.readlines()[-5:]

    alerts = "".join(alerts).strip()

    if not alerts:
        print("⚠️ file.txt is empty (no alerts).")
        return

    try:
        print("📡 Sending alerts to AI for analysis...\n")
        answer = ask_model(f"Analyze these firewall alerts:\n{alerts}")
        print(f"AI Response:\n{answer}\n")
    except Exception as e:
        print(f"⚠️ Error: {e}")

# =============== SERVER CHAT MODE (NEW) ===============
def timestamp():
    return datetime.datetime.now().strftime("[%H:%M:%S]")

def handle_client(conn, addr, history):
    conn.send(b"Connected to CyberGuard Chat! Type 'exit' to quit.\n")
    try:
        while True:
            conn.send(b">>> ")
            data = conn.recv(1024).decode().strip()
            if not data or data.lower() in {"exit", "quit"}:
                break

            print(f"{timestamp()} [{addr[0]}] 💬 {data}")

            # Get GPT response
            try:
                answer = ask_model(data, history)
            except Exception as e:
                error_msg = f"{timestamp()} ⚠️ Error: {e}"
                conn.send(error_msg.encode() + b"\n")
                print(error_msg)
                continue

            response = f"gpt: {answer}\n"

            # Update chat history
            history.append({"role": "user", "content": data})
            history.append({"role": "assistant", "content": answer})

            # Broadcast to all clients
            for c in clients:
                try:
                    c.send(f"\n{timestamp()} [{addr[0]}]: {data}\n{response}\n".encode())
                except:
                    pass

            # Log GPT reply on host
            print(f"{timestamp()} [GPT → all] 🧠 {answer}\n")

    finally:
        conn.close()
        if conn in clients:
            clients.remove(conn)
        print(f"{timestamp()} ❌ {addr[0]} disconnected.")

def start_server(host="0.0.0.0", port=8080):
    global clients
    clients = []
    history = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print(f"{timestamp()} 🌐 CyberGuard chat server running on port {port}")
        
    try:    
        while True:
            conn, addr = s.accept()
            clients.append(conn)
            print(f"{timestamp()} 🔗 {addr[0]} connected.")
            threading.Thread(target=handle_client, args=(conn, addr, history), daemon=True).start()
    except KeyboardInterrupt:
        print(f"\n{timestamp()} SERVER STOPED BY ADMIN.")
        s.close()

# =============== MAIN HANDLER ===============
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 cyberguard.py <prompt>")
        print("  python3 cyberguard.py --chat")
        print("  python3 cyberguard.py response")
        print("  python3 cyberguard.py --server")
        sys.exit(1)

    if sys.argv[1] == "--chat":
        chat_mode()
    elif sys.argv[1] == "response":
        response()
    elif sys.argv[1] == "--server":
        start_server()
    else:
        prompt = " ".join(sys.argv[1:])
        try:
            answer = ask_model(prompt)
            print(answer)
        except Exception as e:
            print(f" Error: {e}")

