# 💰 Luna Noir Upsell & Monetization System

## Overview

Luna Noir now has a comprehensive **3-tier subscription system** with **pay-per-image credits** and a **free trial** to maximize conversions and revenue.

---

## 📊 Monetization Strategy

### 1. **Free Trial** (Hook Users)
- **3 days** of full Premium access
- **5 FREE AI images** included
- All premium features unlocked
- **No credit card required**
- Automatically offered after 3-5 messages

### 2. **Tiered Subscriptions** (Recurring Revenue)

#### 💜 **Basic Premium - $9.99/month**
Perfect for casual users who want NSFW content.

**Features:**
- ✅ NSFW & FLIRTY modes unlocked
- ✅ 20 AI images per month
- ✅ Voice messages enabled
- ✅ Longer conversations (8 turns)
- ✅ Priority response time

**Target Audience:** Users who want NSFW but don't need unlimited images

---

#### 💎 **VIP Premium - $19.99/month** ⭐ MOST POPULAR
Best value for power users.

**Features:**
- ✅ Everything in Basic
- ✅ **UNLIMITED AI images**
- ✅ Custom outfit requests
- ✅ Exclusive VIP scenes
- ✅ Extended memory (16 turns)
- ✅ Early access to new features

**Target Audience:** Power users who generate lots of images

---

#### 👑 **Ultimate - $49.99/month**
For superfans and whales.

**Features:**
- ✅ Everything in VIP
- ✅ **UNLIMITED everything**
- ✅ Custom image prompts
- ✅ Video messages (coming soon)
- ✅ 1-on-1 priority support
- ✅ Request custom features
- ✅ Your name in credits

**Target Audience:** Superfans, whales, users who want VIP treatment

---

### 3. **Pay-Per-Image Credits** (One-Time Revenue)
For users who don't want subscriptions.

| Pack | Credits | Price | Bonus | Best For |
|------|---------|-------|-------|----------|
| **Starter** | 5 images | $2.99 | - | Trying it out |
| **Standard** | 20 images | $9.99 | - | Occasional use |
| **Value** | 50 images | $19.99 | +10 FREE | Heavy users |

**Note:** VIP subscription ($19.99/mo) gives UNLIMITED images, making it better value than buying credits repeatedly.

---

## 🎯 Strategic Upsell Triggers

### When Users Hit Limits

1. **Image Generation Limit Reached**
   - Basic users: Upsell to VIP for unlimited
   - Free users: Show all plans + credit packs

2. **NSFW Mode Locked**
   - Offer free trial first
   - Then show subscription plans

3. **Voice Messages Locked**
   - Offer free trial
   - Highlight voice as premium feature

4. **Conversation Limit**
   - Free users get 2-turn memory
   - Upsell to Premium for 8-16 turns

### Periodic Reminders

- **After 3-5 messages**: Offer free trial to new users
- **Every 20 messages**: Gentle upgrade reminder for free users
- **After generating image**: Subtle reminder of remaining images

---

## 💳 Stripe Integration

### Required Stripe Products

You need to create these products in your Stripe Dashboard:

#### Subscription Products (Recurring)
1. **Basic Premium** - $9.99/month
   - Price ID: `price_basic_monthly`
   
2. **VIP Premium** - $19.99/month
   - Price ID: `price_vip_monthly`
   
3. **Ultimate** - $49.99/month
   - Price ID: `price_ultimate_monthly`

#### One-Time Products (Credits)
1. **5 Image Credits** - $2.99
   - Price ID: `price_5_images`
   
2. **20 Image Credits** - $9.99
   - Price ID: `price_20_images`
   
3. **50 Image Credits** - $19.99
   - Price ID: `price_50_images`

### Environment Variables

Add these to your `.env` file:

```bash
# Stripe Keys
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Subscription Price IDs
STRIPE_BASIC_PRICE_ID=price_basic_monthly
STRIPE_VIP_PRICE_ID=price_vip_monthly
STRIPE_ULTIMATE_PRICE_ID=price_ultimate_monthly

# Credit Pack Price IDs
STRIPE_5_IMAGES_PRICE_ID=price_5_images
STRIPE_20_IMAGES_PRICE_ID=price_20_images
STRIPE_50_IMAGES_PRICE_ID=price_50_images

# Payment URLs
SUCCESS_URL=https://t.me/Lunanoircompanionbot?start=payment_success
CANCEL_URL=https://t.me/Lunanoircompanionbot?start=payment_cancelled
```

---

## 🔧 How It Works

### For Users

1. **New User Flow:**
   ```
   User starts bot → Chats 3-5 messages → Offered FREE trial
   → Accepts trial → Gets 3 days + 5 images
   → Trial ends → Prompted to subscribe or buy credits
   ```

2. **Image Generation Flow:**
   ```
   User clicks "Generate Image"
   → System checks: Subscription? Credits? Trial?
   → If yes: Generate image, deduct from quota
   → If no: Show upsell (plans or credits)
   → After generation: Show remaining images + subtle upsell
   ```

3. **NSFW Mode Flow:**
   ```
   User tries NSFW mode
   → Check if premium/trial
   → If no: Show free trial offer
   → If trial used: Show subscription plans
   ```

### For Developers

The system automatically:
- ✅ Tracks subscription status and expiration
- ✅ Counts monthly image usage per plan
- ✅ Manages credit balances
- ✅ Handles free trial eligibility
- ✅ Shows appropriate upsells at the right time
- ✅ Deducts from subscription → credits → trial (in that order)

---

## 📁 File Structure

```
src/payment/
├── __init__.py              # Module exports
├── upsell.py                # Core subscription & credit logic
└── upsell_prompts.py        # Upsell messages & UI

data/
├── subscriptions.json       # User subscription data
├── credits.json             # User credit balances
└── trials.json              # Free trial tracking
```

---

## 🎨 User Interface

### Main Menu
```
📸 Generate Image
🎧 Voice Settings
🎮 Profile & XP
🎯 Change Mode
💎 Premium  ← Shows plan comparison
❓ Help
```

### Premium Menu
```
💎 Premium Features

✅ NSFW & FLIRTY modes
✅ Longer conversations
✅ Voice replies
✅ AI-generated images
✅ Priority support

[💎 Upgrade Now] [« Back]
```

### Plans Comparison
```
💎 Premium Plans

💜 BASIC - $9.99/month
✅ NSFW & FLIRTY modes
✅ 20 AI images/month
✅ Voice messages
...

[💜 Basic ($9.99/mo)]
[💎 VIP ($19.99/mo) ⭐]
[👑 Ultimate ($49.99/mo)]
[🎫 Buy Credits Instead]
```

---

## 📈 Revenue Projections

### Conservative Estimates

**Assumptions:**
- 1000 monthly active users
- 5% conversion to paid (50 users)
- 60% Basic, 30% VIP, 10% Ultimate

**Monthly Recurring Revenue:**
- Basic: 30 users × $9.99 = $299.70
- VIP: 15 users × $19.99 = $299.85
- Ultimate: 5 users × $49.99 = $249.95
- **Total MRR: $849.50**

**One-Time Credit Sales:**
- Estimate 20 credit purchases/month
- Average $10 per purchase
- **Monthly Credits Revenue: $200**

**Total Monthly Revenue: ~$1,050**

### Growth Scenario (10,000 MAU)
- 10% conversion rate (1000 paid users)
- **Estimated MRR: $15,000 - $20,000**

---

## 🚀 Next Steps

### 1. Set Up Stripe Products
- Create all 6 products in Stripe Dashboard
- Copy Price IDs to `.env` file

### 2. Test Payment Flow
- Use Stripe test mode
- Test each subscription tier
- Test credit pack purchases
- Verify webhooks work

### 3. Launch Free Trial
- Monitor conversion rates
- A/B test trial duration (3 vs 7 days)
- Track which features drive conversions

### 4. Optimize Pricing
- Monitor churn rates
- Test different price points
- Add annual plans (20% discount)

### 5. Add Features
- Implement video messages for Ultimate
- Add custom prompt builder
- Create VIP-only scenes

---

## 💡 Tips for Maximizing Revenue

1. **Make Free Trial Irresistible**
   - No credit card required
   - Full access to everything
   - 5 free images to get hooked

2. **Show Value Clearly**
   - "VIP = UNLIMITED images for $19.99"
   - "That's less than $1 per image if you use 20+"

3. **Create FOMO**
   - "Trial ending in 1 day!"
   - "Only 3 images left!"

4. **Upsell at Right Moments**
   - After they love an image → "Want unlimited?"
   - When they hit limit → "Upgrade for more!"

5. **Make VIP the Obvious Choice**
   - Mark as "MOST POPULAR"
   - Show it's better value than credits
   - Highlight unlimited images

---

## 🔒 Security Notes

- Never store credit card info (Stripe handles it)
- Use Stripe webhooks to verify payments
- Validate all subscription status server-side
- Rate limit API calls to prevent abuse

---

## 📞 Support

For questions about the upsell system:
1. Check `src/payment/upsell.py` for subscription logic
2. Check `src/payment/upsell_prompts.py` for UI messages
3. Review Stripe Dashboard for payment status

---

**Built with 💜 for Luna Noir**

