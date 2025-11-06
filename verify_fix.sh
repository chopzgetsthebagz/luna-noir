#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         LUNA NOIR - OPENAI API KEY VERIFICATION SCRIPT         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Load environment
source .env

echo "=== STEP 1: CHECK API KEY ===" 
echo "API Key length: ${#OPENAI_API_KEY} characters"
echo "API Key: ${OPENAI_API_KEY:0:20}...${OPENAI_API_KEY: -4}"
echo "Model: $OPENAI_MODEL"
echo ""

echo "=== STEP 2: TEST OPENAI API ===" 
python3 << 'PYEOF'
import os
import requests

api_key = os.getenv("OPENAI_API_KEY")
url = "https://api.openai.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
payload = {
    "model": "gpt-4-turbo-preview",
    "messages": [{"role": "user", "content": "Say 'API test successful'"}],
    "max_tokens": 10
}

try:
    resp = requests.post(url, headers=headers, json=payload, timeout=15)
    if resp.status_code == 200:
        print("✅ OpenAI API key is VALID and WORKING!")
        result = resp.json()
        print(f"   Response: {result['choices'][0]['message']['content']}")
    elif resp.status_code == 401:
        print("❌ 401 Unauthorized - API key is INVALID or REVOKED")
        print(f"   {resp.json().get('error', {}).get('message', 'Unknown error')}")
    else:
        print(f"❌ Error {resp.status_code}")
        print(f"   {resp.text[:200]}")
except Exception as e:
    print(f"❌ Exception: {e}")
PYEOF

echo ""
echo "=== STEP 3: CHECK FLASK STATUS ===" 
FLASK_PID=$(lsof -ti:5050 2>/dev/null | head -1)
if [ -n "$FLASK_PID" ]; then
    echo "✅ Flask is running (PID: $FLASK_PID)"
else
    echo "❌ Flask is NOT running on port 5050"
    echo "   Run: source .venv/bin/activate && make run"
fi

echo ""
echo "=== STEP 4: CHECK NGROK STATUS ===" 
NGROK_PID=$(pgrep -f "ngrok http" | head -1)
if [ -n "$NGROK_PID" ]; then
    echo "✅ ngrok is running (PID: $NGROK_PID)"
    PUBLIC_URL=$(curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null | python3 -c "import sys, json; t=json.load(sys.stdin); print([x['public_url'] for x in t.get('tunnels',[]) if x.get('public_url','').startswith('https://')][0])" 2>/dev/null)
    echo "   Public URL: $PUBLIC_URL"
else
    echo "❌ ngrok is NOT running"
    echo "   Run: ngrok http 5050"
fi

echo ""
echo "=== NEXT STEPS ===" 
echo "1. If OpenAI API test passed: ✅ API key is working!"
echo "2. If Flask is not running: Restart it with 'make run'"
echo "3. Send a test message to @Lunanoircompanionbot on Telegram"
echo "4. Check Flask logs for any errors"
echo ""

