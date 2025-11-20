# 🧪 Luna Noir - Test Mode Guide

## What is Test Mode?

Test mode allows you to **test the entire payment and monetization system** without setting up Stripe or charging real money. Perfect for:

- Testing the user experience
- Demoing the bot to potential users
- Verifying upsell prompts work
- Testing image generation limits
- Testing premium feature unlocking

---

## 🎮 Test Commands

### **Get Help**
```
/testhelp
```
Shows all available test commands.

---

### **Simulate Subscription Purchase**

Buy a premium subscription (test mode - no real money):

```
/testbuy basic      # Basic Premium - $9.99/mo
/testbuy vip        # VIP Premium - $19.99/mo
/testbuy ultimate   # Ultimate - $49.99/mo
```

**What you get:**
- **Basic:** NSFW mode, 20 images/month, voice messages
- **VIP:** Everything in Basic + UNLIMITED images, custom outfits
- **Ultimate:** UNLIMITED everything, custom prompts, priority support

---

### **Simulate Credit Purchase**

Buy image credits (test mode - no real money):

```
/testbuy 5pack      # 5 image credits - $2.99
/testbuy 20pack     # 20 image credits - $9.99
/testbuy 50pack     # 60 image credits - $19.99 (50 + 10 bonus)
```

---

### **Start Free Trial**

Activate the 3-day free trial:

```
/testtrial
```

**You get:**
- 3 days of Premium access
- 5 FREE AI images
- All premium features unlocked
- No credit card required

---

### **Reset Everything**

Clear all your test purchases and start fresh:

```
/testreset
```

This removes:
- All subscriptions
- All credits
- Trial status

Perfect for testing the flow multiple times!

---

## 📋 Testing Workflow

### **Test 1: Free User Experience**

1. Send `/start` to Luna
2. Try to generate an image → Should see upsell message
3. Try to switch to NSFW mode → Should see upsell message

### **Test 2: Free Trial Flow**

1. Send `/testtrial` → Activate free trial
2. Send `/generate` → Should work! (5 images available)
3. Generate 5 images → Trial images exhausted
4. Try to generate again → Should see upsell to subscribe

### **Test 3: Basic Subscription**

1. Send `/testbuy basic` → Get Basic Premium
2. Send `/generate` → Should work! (20 images/month)
3. Switch to NSFW mode → Should work!
4. Generate 20 images → Monthly limit reached
5. Try to generate again → Should see upsell to VIP

### **Test 4: VIP Subscription**

1. Send `/testreset` → Clear previous purchases
2. Send `/testbuy vip` → Get VIP Premium
3. Send `/generate` → Should work! (UNLIMITED)
4. Generate 100 images → Should never hit limit!

### **Test 5: Credit Packs**

1. Send `/testreset` → Clear previous purchases
2. Send `/testbuy 5pack` → Get 5 credits
3. Send `/generate` → Should work! (5 images available)
4. Generate 5 images → Credits exhausted
5. Send `/testbuy 20pack` → Get 20 more credits
6. Check `/profile` → Should show 20 credits

---

## 🎯 What to Test

### **Upsell Messages**
- [ ] Image limit reached message
- [ ] NSFW mode locked message
- [ ] Free trial offer (after 3-5 messages)
- [ ] After-image upsell (after generating)
- [ ] Plans comparison message
- [ ] Credits shop message

### **Premium Features**
- [ ] NSFW mode unlocks with subscription
- [ ] Image generation works with credits
- [ ] Image generation works with subscription
- [ ] Monthly limits enforced (Basic plan)
- [ ] Unlimited images work (VIP/Ultimate)
- [ ] Voice messages unlock with premium

### **Payment Flow**
- [ ] Free trial activation
- [ ] Subscription purchase
- [ ] Credit pack purchase
- [ ] Trial expiration handling
- [ ] Subscription expiration handling

---

## 🚀 Next Steps (Real Payments)

Once you've tested everything and are happy with the flow:

1. **Create Stripe account** at https://stripe.com
2. **Create products** in Stripe Dashboard
3. **Add Stripe keys** to `.env` file
4. **Uncomment payment code** in `src/core/bot.py`
5. **Test with Stripe test mode** first
6. **Switch to live mode** when ready
7. **Deploy to Railway** for 24/7 uptime

---

## 💡 Tips

- Use `/testreset` frequently to test different scenarios
- Test the free trial → subscription upgrade path
- Test running out of credits/images
- Test all upsell messages
- Make sure NSFW mode is properly gated
- Verify image limits are enforced correctly

---

**Happy testing! 🎉**

