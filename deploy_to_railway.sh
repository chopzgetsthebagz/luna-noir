#!/bin/bash

# 🚀 Quick Railway Deployment Script for Luna Noir Bot

echo "🚀 Luna Noir Bot - Railway Deployment Helper"
echo "=============================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Prepare for Railway deployment"
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Check if remote is set
if ! git remote | grep -q "origin"; then
    echo ""
    echo "⚠️  No git remote found!"
    echo "Please create a GitHub repository and run:"
    echo ""
    echo "  git remote add origin https://github.com/YOUR_USERNAME/luna-noir-bot.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    echo ""
else
    echo "✅ Git remote configured"
    echo ""
    echo "📤 Pushing to GitHub..."
    git add .
    git commit -m "Update for Railway deployment" || echo "No changes to commit"
    git push origin main || git push origin master
    echo "✅ Code pushed to GitHub"
fi

echo ""
echo "=============================================="
echo "🎯 Next Steps:"
echo "=============================================="
echo ""
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select 'luna-noir-bot'"
echo ""
echo "5. Add these environment variables in Railway:"
echo "   - TELEGRAM_BOT_TOKEN=your_telegram_bot_token"
echo "   - GROQ_API_KEY=your_groq_api_key"
echo "   - LLM_PROVIDER=groq"
echo "   - MODEL_PROVIDER=groq"
echo "   - GROQ_MODEL=llama-3.3-70b-versatile"
echo "   - SAFETY_MODE=off"
echo "   - DEFAULT_MODE=NSFW"
echo "   - FLASK_HOST=0.0.0.0"
echo "   - FLASK_DEBUG=False"
echo ""
echo "6. After deployment, get your Railway URL"
echo "7. Update Telegram webhook:"
echo ""
echo "   curl -X POST 'https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook' \\"
echo "     -d 'url=https://YOUR-RAILWAY-URL.up.railway.app/webhook'"
echo ""
echo "8. Test your bot on Telegram!"
echo ""
echo "=============================================="
echo "📖 Full guide: See RAILWAY_DEPLOYMENT.md"
echo "=============================================="

