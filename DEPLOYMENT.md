# 🚀 Luna Noir Deployment Guide

## Why Does Luna Stop When I Close My Laptop?

The bot stops because it's running as a **foreground process** in your terminal. When you close your laptop:
- Mac goes to sleep → All processes pause
- Terminal closes → Python process gets killed
- No server running → Bot can't receive messages

---

## 🌐 Solution 1: Deploy to Cloud (RECOMMENDED)

Deploy Luna to a server that runs 24/7.

### Option A: Railway.app (Easiest)

**Pros:** Free tier, auto-deploys from GitHub, super easy
**Cons:** Free tier has limits

**Steps:**

1. **Create `Procfile` in your project root:**
```
web: python src/server/app.py
```

2. **Create `railway.json`:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python src/server/app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

3. **Go to [Railway.app](https://railway.app)**
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `luna-noir-bot`
   - Add environment variables from `.env`
   - Deploy!

4. **Update Webhook URL:**
   - Copy your Railway URL (e.g., `https://luna-noir-bot-production.up.railway.app`)
   - Update `WEBHOOK_URL` in Railway environment variables
   - Restart the service

---

### Option B: Render.com (Also Easy)

**Pros:** Free tier, auto-deploys, good for Python
**Cons:** Free tier sleeps after 15 min inactivity

**Steps:**

1. **Create `render.yaml` in project root:**
```yaml
services:
  - type: web
    name: luna-noir-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/server/app.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: ELEVENLABS_API_KEY
        sync: false
      - key: STRIPE_SECRET_KEY
        sync: false
```

2. **Go to [Render.com](https://render.com)**
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Add environment variables
   - Deploy!

---

### Option C: DigitalOcean ($5/month)

**Pros:** Full control, always on, fast
**Cons:** Costs $5/month

**Steps:**

1. **Create a Droplet:**
   - Go to [DigitalOcean](https://www.digitalocean.com)
   - Create a $5/month Ubuntu droplet
   - SSH into it: `ssh root@your_droplet_ip`

2. **Install Dependencies:**
```bash
# Update system
apt update && apt upgrade -y

# Install Python 3.9+
apt install python3 python3-pip python3-venv git -y

# Clone your repo
git clone https://github.com/chopzgetsthebagz/luna-noir.git
cd luna-noir

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

3. **Create `.env` file:**
```bash
nano .env
# Paste your environment variables
# Save with Ctrl+X, Y, Enter
```

4. **Run with systemd (keeps it running):**
```bash
# Create service file
nano /etc/systemd/system/luna-bot.service
```

Paste this:
```ini
[Unit]
Description=Luna Noir Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/luna-noir
Environment="PYTHONPATH=/root/luna-noir"
ExecStart=/root/luna-noir/.venv/bin/python /root/luna-noir/src/server/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

5. **Start the service:**
```bash
systemctl daemon-reload
systemctl enable luna-bot
systemctl start luna-bot

# Check status
systemctl status luna-bot

# View logs
journalctl -u luna-bot -f
```

---

## 💻 Solution 2: Run as Background Service on Mac

Keep Luna running on your Mac even when you close the lid.

### Steps:

1. **Create logs directory:**
```bash
mkdir -p /Users/karimhassan/Desktop/luna-noir-bot/logs
```

2. **Install the LaunchAgent:**
```bash
# Copy the plist file to LaunchAgents
cp com.luna.bot.plist ~/Library/LaunchAgents/

# Load the service
launchctl load ~/Library/LaunchAgents/com.luna.bot.plist

# Start the service
launchctl start com.luna.bot
```

3. **Check if it's running:**
```bash
# Check status
launchctl list | grep luna

# View logs
tail -f logs/bot.log
tail -f logs/bot.error.log
```

4. **Prevent Mac from sleeping:**
```bash
# Keep Mac awake while plugged in
sudo pmset -c sleep 0
sudo pmset -c displaysleep 10

# Or use caffeinate
caffeinate -s
```

### Manage the Service:

```bash
# Stop the bot
launchctl stop com.luna.bot

# Unload the service
launchctl unload ~/Library/LaunchAgents/com.luna.bot.plist

# Reload after changes
launchctl unload ~/Library/LaunchAgents/com.luna.bot.plist
launchctl load ~/Library/LaunchAgents/com.luna.bot.plist
```

**Downsides:**
- Mac must stay on 24/7
- Uses electricity (~$5-10/month)
- Not as reliable as cloud hosting
- If Mac crashes, bot goes down

---

## 🔧 Solution 3: Use Screen/Tmux (Quick Fix)

Run the bot in a persistent terminal session.

### Using `screen`:

```bash
# Install screen (if not installed)
brew install screen

# Start a new screen session
screen -S luna-bot

# Run the bot
cd /Users/karimhassan/Desktop/luna-noir-bot
source .venv/bin/activate
PYTHONPATH=/Users/karimhassan/Desktop/luna-noir-bot python src/server/app.py

# Detach from screen: Press Ctrl+A, then D

# Reattach later
screen -r luna-bot

# List all screens
screen -ls

# Kill a screen
screen -X -S luna-bot quit
```

### Using `tmux`:

```bash
# Install tmux
brew install tmux

# Start a new tmux session
tmux new -s luna-bot

# Run the bot
cd /Users/karimhassan/Desktop/luna-noir-bot
source .venv/bin/activate
PYTHONPATH=/Users/karimhassan/Desktop/luna-noir-bot python src/server/app.py

# Detach from tmux: Press Ctrl+B, then D

# Reattach later
tmux attach -t luna-bot

# List all sessions
tmux ls

# Kill a session
tmux kill-session -t luna-bot
```

**Downsides:**
- Still requires Mac to stay awake
- Session dies if Mac restarts

---

## 📊 Comparison

| Solution | Cost | Reliability | Ease | Best For |
|----------|------|-------------|------|----------|
| **Railway.app** | Free | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Production |
| **Render.com** | Free | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Testing |
| **DigitalOcean** | $5/mo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Production |
| **Mac LaunchAgent** | $0 | ⭐⭐⭐ | ⭐⭐⭐ | Development |
| **Screen/Tmux** | $0 | ⭐⭐ | ⭐⭐⭐⭐ | Quick testing |

---

## 🎯 Recommended Approach

**For Production (Real Users):**
1. Deploy to **Railway.app** (free, easy, reliable)
2. Or use **DigitalOcean** ($5/month, full control)

**For Development/Testing:**
1. Use **screen** or **tmux** for quick testing
2. Or run as **LaunchAgent** on your Mac

---

## 🚨 Important Notes

### If Using Cloud Hosting:

1. **Update Webhook URL:**
   - Your webhook URL will change from ngrok to your cloud URL
   - Update `WEBHOOK_URL` in environment variables
   - Example: `https://luna-noir-bot.up.railway.app/webhook`

2. **Set Webhook:**
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-cloud-url.com/webhook"
```

3. **Environment Variables:**
   - Make sure ALL variables from `.env` are set in cloud platform
   - Don't commit `.env` to GitHub!

4. **Database:**
   - Your JSON files (`data/*.json`) won't persist on free tiers
   - Consider using a real database (PostgreSQL, MongoDB)
   - Or use cloud storage (S3, Google Cloud Storage)

---

## 🔐 Security Tips

1. **Never commit `.env` to GitHub**
   - Already in `.gitignore`
   - Double-check before pushing

2. **Use environment variables in cloud**
   - Don't hardcode secrets
   - Use platform's environment variable settings

3. **Enable HTTPS**
   - Telegram requires HTTPS for webhooks
   - Cloud platforms provide this automatically

4. **Rotate API keys regularly**
   - Change Telegram bot token if exposed
   - Rotate Stripe keys periodically

---

## 📞 Need Help?

If you run into issues:
1. Check logs: `tail -f logs/bot.log`
2. Test webhook: `curl https://your-url.com/webhook`
3. Verify environment variables are set
4. Check Telegram webhook status:
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
   ```

---

**🚀 Ready to deploy? I recommend starting with Railway.app - it's the easiest!**

