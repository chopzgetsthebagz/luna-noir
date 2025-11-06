#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate
pkill -f "flask --app src/server/app" || true
(flask --app src/server/app run --port 5050 --debug &) 
sleep 2
pgrep -f "ngrok http 5050" >/dev/null || (ngrok http 5050 >/dev/null &)
sleep 2
URL=$(curl -s http://127.0.0.1:4040/api/tunnels | python3 -c "import sys, json; t=json.load(sys.stdin)['tunnels']; print([x['public_url'] for x in t if x['public_url'].startswith('https://')][0])")
WEBHOOK_URL="$URL/webhook"
TOKEN=$(grep -E '^TELEGRAM_TOKEN=' .env | cut -d= -f2)
curl -s -X POST "https://api.telegram.org/bot$TOKEN/setWebhook" -d "url=$WEBHOOK_URL" >/dev/null
echo "Webhook set to: $WEBHOOK_URL"

