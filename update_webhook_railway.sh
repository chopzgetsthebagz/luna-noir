#!/bin/bash

# Update Telegram webhook to Railway URL
# Replace YOUR-RAILWAY-URL with your actual Railway domain

echo "🔧 Updating Telegram webhook to Railway..."
echo ""
echo "⚠️  IMPORTANT: Replace YOUR-RAILWAY-URL with your actual Railway domain!"
echo "Example: luna-noir-production-xxxx.up.railway.app"
echo ""
read -p "Enter your Railway URL (without https://): " RAILWAY_URL

if [ -z "$RAILWAY_URL" ]; then
    echo "❌ Error: Railway URL cannot be empty"
    exit 1
fi

WEBHOOK_URL="https://${RAILWAY_URL}/webhook"
BOT_TOKEN="7576467529:AAHWymLnJtqIe1TFizxAKMUdG63b2fB0-7g"

echo ""
echo "Setting webhook to: $WEBHOOK_URL"
echo ""

# Set the webhook
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
  -d "url=${WEBHOOK_URL}"

echo ""
echo ""
echo "✅ Webhook updated!"
echo ""
echo "Verifying webhook status..."
echo ""

# Verify webhook
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -m json.tool

echo ""
echo "🎉 Done! Your bot should now be running on Railway 24/7!"
echo ""
echo "📝 Next steps:"
echo "1. Go back to Railway and add this variable:"
echo "   WEBHOOK_URL=${WEBHOOK_URL}"
echo ""
echo "2. Test your bot on Telegram - send /start"
echo ""
echo "3. Close your laptop - Luna will keep running! 🚀"

