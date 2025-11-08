# 🚀 Deploy Luna Noir Bot to Railway

## Step 1: Push Code to GitHub

First, make sure your code is on GitHub:

```bash
# If you haven't initialized git yet:
git init
git add .
git commit -m "Prepare for Railway deployment"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/luna-noir-bot.git
git branch -M main
git push -u origin main
```

## Step 2: Sign Up for Railway

1. Go to **https://railway.app**
2. Click **"Login"** or **"Start a New Project"**
3. Sign up with **GitHub** (easiest option)
4. Authorize Railway to access your GitHub repos

## Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **"luna-noir-bot"** from the list
4. Railway will automatically detect it's a Python app

## Step 4: Configure Environment Variables

Click on your project → **"Variables"** tab → Add these variables:

### Required Variables:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_api_key_here

LLM_PROVIDER=groq
MODEL_PROVIDER=groq
GROQ_MODEL=llama-3.3-70b-versatile

SAFETY_MODE=off
DEFAULT_MODE=NSFW

FLASK_HOST=0.0.0.0
FLASK_DEBUG=False

# Voice/TTS (Optional - for voice replies)
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=Rachel
VOICE_ENABLED_DEFAULT=true
```

### Optional Variables (if you use them):

```
ELEVENLABS_API_KEY=your_elevenlabs_key
OPENROUTER_API_KEY=your_openrouter_key
STRIPE_SECRET_KEY=your_stripe_key
```

## Step 5: Get Your Railway URL

1. After deployment, Railway will give you a URL like:
   `https://luna-noir-bot-production.up.railway.app`
2. Copy this URL - you'll need it for the webhook

## Step 6: Update Telegram Webhook

Once deployed, update your Telegram webhook to point to Railway:

```bash
curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook" \
  -d "url=https://YOUR-RAILWAY-URL.up.railway.app/webhook"
```

Replace `YOUR-RAILWAY-URL` with your actual Railway URL.

## Step 7: Verify Deployment

Check if the webhook is set correctly:

```bash
curl "https://api.telegram.org/botYOUR_BOT_TOKEN/getWebhookInfo"
```

You should see your Railway URL in the response.

## Step 8: Test the Bot

Send a message to your bot on Telegram - it should respond!

---

## 🔍 Monitoring & Logs

### View Logs:
1. Go to your Railway project
2. Click on the service
3. Click **"Deployments"** → Select latest deployment
4. Click **"View Logs"** to see real-time logs

### Check Status:
- Green dot = Running ✅
- Red dot = Failed ❌
- Yellow dot = Building 🔨

---

## 💰 Railway Pricing

**Free Tier**:
- $5 credit per month
- Enough for ~500 hours of runtime
- Perfect for small bots

**Pro Plan** ($20/month):
- Unlimited usage
- Better performance
- Priority support

---

## 🔧 Troubleshooting

### Bot not responding?
1. Check Railway logs for errors
2. Verify webhook is set correctly: `getWebhookInfo`
3. Check environment variables are set

### Deployment failed?
1. Check Railway build logs
2. Make sure `requirements.txt` is up to date
3. Verify `Procfile` is correct

### Out of credits?
1. Upgrade to Pro plan ($20/month)
2. Or use a different service (Render, Fly.io)

---

## 🎉 You're Done!

Your bot is now running 24/7 on Railway! No more ngrok, no more keeping your laptop on.

**Next Steps**:
- Monitor usage in Railway dashboard
- Set up alerts for errors
- Add more features to Luna!

---

## 📝 Notes

- Railway auto-deploys when you push to GitHub
- No need to manually restart after code changes
- Free tier is perfect for testing and small bots
- Upgrade to Pro if you need more resources

**Enjoy your 24/7 Luna Noir bot! 🔥😈**
