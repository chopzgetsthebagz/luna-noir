#!/usr/bin/env bash
set -euo pipefail

# Load .env
if [ -f ".env" ]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' .env | xargs)
else
  echo ".env not found. Put TELEGRAM_TOKEN in it."
  exit 1
fi

# Grab current HTTPS tunnel from ngrok local API
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels \
  | python3 -c "import sys, json; t=json.load(sys.stdin); print([x['public_url'] for x in t.get('tunnels',[]) if x.get('public_url','').startswith('https://')][0])")

if [ -z "${NGROK_URL:-}" ]; then
  echo "No ngrok https tunnel found. Start it with: ngrok http 5050"
  exit 1
fi

WEBHOOK_URL="${NGROK_URL}/webhook"
echo "Setting webhook to: ${WEBHOOK_URL}"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/setWebhook" \
  -F "url=${WEBHOOK_URL}" \
  && echo -e "\nDone."

echo "Current webhook info:"
curl -s "https://api.telegram.org/bot${TELEGRAM_TOKEN}/getWebhookInfo"
echo
