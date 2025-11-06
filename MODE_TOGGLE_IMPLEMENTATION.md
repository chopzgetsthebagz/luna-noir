# Luna Noir - Mode Toggle Implementation

## ✅ IMPLEMENTATION COMPLETE

### Overview
Added three conversation modes (SAFE, FLIRTY, NSFW) with per-user persistence, inline keyboard controls, and mode-specific system prompts.

---

## FILES CHANGED

### ✅ Modified Files

1. **`src/utils/md.py`**
   - Added `render_markdown(text: str) -> str` function
   - Provides single place to tweak text formatting (currently pass-through)

2. **`src/core/bot.py`**
   - Added mode constants: `MODE_SAFE`, `MODE_FLIRTY`, `MODE_NSFW`
   - Added `USER_MODES_PATH = Path("data/memory/user_modes.json")`
   - Added mode management functions:
     * `get_user_mode(user_id) -> str` - Get user's current mode (defaults to SAFE)
     * `set_user_mode(user_id, mode)` - Set user's mode with atomic file write
     * `build_mode_keyboard(current_mode) -> InlineKeyboardMarkup` - Create inline buttons
     * `get_mode_system_prompt(mode) -> str` - Get mode-specific system prompt
   - Updated `/start` command - Shows current mode + inline keyboard
   - Updated `/help` command - Added mode descriptions
   - Added `/mode` command - Show mode selector with descriptions
   - Added `mode_callback()` handler - Handle inline button clicks
   - Updated `on_text()` handler:
     * Reads user mode before generating response
     * Uses mode-specific system prompt
     * Shows typing indicator
     * Uses `render_markdown()` before sending
   - Registered `CallbackQueryHandler` for mode buttons

### ✅ Created Files

1. **`data/memory/user_modes.json`**
   - Stores user mode preferences
   - Format: `{"<user_id>": "MODE"}`
   - Created automatically on first mode change
   - Atomic writes (write to .tmp then rename)

---

## FEATURES IMPLEMENTED

### 1. Three Modes

#### 🟢 SAFE (Default)
- **Description**: Friendly, SFW conversations
- **System Prompt**: 
  > "You are Luna Noir, a warm, playful, helpful assistant. Be brief, friendly, and proactive. Use emojis occasionally. Stay SFW and friendly. No explicit sexual content."

#### 💛 FLIRTY
- **Description**: Light flirtation, PG-13
- **System Prompt**:
  > "You are Luna Noir, a warm, playful, flirtatious assistant. Be brief, friendly, and proactive. Use emojis occasionally. Light flirtation is allowed. Keep it tasteful and PG-13. No explicit sexual content."

#### 🔴 NSFW (18+ Only)
- **Description**: Adult content
- **System Prompt**:
  > "You are Luna Noir, a warm, playful, sensual companion. Be brief, friendly, and proactive. Use emojis occasionally. Roleplay consented adult erotic content is allowed. REFUSE anything involving: minors, non-consent, real-person porn, or illegal acts. Keep within platform policy limits."

### 2. Commands

| Command | Description |
|---------|-------------|
| `/start` | Wake Luna & see current mode with inline keyboard |
| `/help` | Show commands and mode descriptions |
| `/mode` | Show mode selector with inline keyboard |
| `/menu` | Quick action suggestions |
| `/model` | Show current LLM provider |
| `/upgrade` | Unlock Premium features |
| `/reset` | Clear conversation memory |

### 3. Inline Keyboard

- Three buttons in a single row: `SAFE | FLIRTY | NSFW`
- Current mode marked with ✓ checkmark
- Callback data format: `mode:SAFE`, `mode:FLIRTY`, `mode:NSFW`
- Instant mode switching with confirmation message
- Keyboard updates to reflect new selection

### 4. Per-User Persistence

- **Storage**: `data/memory/user_modes.json`
- **Format**: JSON object mapping user IDs to modes
- **Default**: SAFE mode for new users
- **Atomic Writes**: Write to `.tmp` file then rename (prevents corruption)
- **Thread-Safe**: File locking via atomic rename operation

### 5. Typing Indicator

- Shows "typing..." while LLM generates response
- Sent via `bot.send_chat_action(chat_id, action="typing")`
- Improves user experience during LLM processing

---

## STORAGE LOCATION

**File**: `data/memory/user_modes.json`

**Example Content**:
```json
{
  "123456789": "SAFE",
  "987654321": "FLIRTY",
  "555555555": "NSFW"
}
```

**Directory Structure**:
```
data/
├── memory/
│   ├── user_modes.json          ← Mode preferences
│   ├── <chat_id>.json           ← Conversation history
│   └── user_modes.json.tmp      ← Temp file during writes
└── users.json                   ← Premium user database
```

---

## TESTING

### ✅ All Tests Passed

```
✓ Test 1: Default mode for new user (SAFE)
✓ Test 2: Set mode to FLIRTY
✓ Test 3: Set mode to NSFW
✓ Test 4: Verify persistence in JSON file
✓ Test 5: System prompts for each mode
✓ Test 6: Build inline keyboard (3 buttons, 1 row)
✓ Test 7: Multiple users with different modes
```

### Manual Test Steps

1. **Start the bot**:
   ```bash
   source .venv/bin/activate
   python src/server/app.py
   ```

2. **Test /start command**:
   - Send `/start` to bot on Telegram
   - Should see: "Luna Noir online ✨" with current mode and 3 buttons
   - Default mode should be SAFE

3. **Test mode switching**:
   - Tap "FLIRTY" button
   - Should see: "✅ Mode changed to FLIRTY"
   - Button should now show "✓ FLIRTY"
   - Tap "NSFW" button
   - Should see: "✅ Mode changed to NSFW"
   - Button should now show "✓ NSFW"

4. **Test /mode command**:
   - Send `/mode`
   - Should see mode descriptions and inline keyboard
   - Current mode should be highlighted with ✓

5. **Test /help command**:
   - Send `/help`
   - Should see updated help text with mode descriptions

6. **Test conversation with different modes**:
   - Set mode to SAFE, send a message
   - Bot should respond in friendly, SFW manner
   - Set mode to FLIRTY, send a message
   - Bot should respond with light flirtation
   - Set mode to NSFW, send a message
   - Bot should respond with adult content (if appropriate)

7. **Test persistence**:
   - Change mode to FLIRTY
   - Restart the bot
   - Send `/start`
   - Mode should still be FLIRTY

8. **Verify file creation**:
   ```bash
   cat data/memory/user_modes.json
   ```
   - Should see your user ID with selected mode

---

## INTEGRATION WITH EXISTING FEATURES

### ✅ Premium Gate
- Mode selection works for all users
- Only premium users can chat (existing behavior)
- Free users see upgrade message (unchanged)

### ✅ Conversation Memory
- Mode does NOT affect conversation history
- Each mode uses same memory file: `data/memory/<chat_id>.json`
- Premium users: 16 messages (8 turns) retained
- Mode only affects system prompt, not memory

### ✅ Multi-Provider LLM
- Works with OpenAI, OpenRouter, Groq
- Mode system prompt prepended to all LLM calls
- No provider-specific changes needed

### ✅ Stripe Integration
- Mode preferences independent of subscription status
- Premium users can use any mode
- Free users can set mode but can't chat

---

## SAFETY & COMPLIANCE

### Content Moderation

1. **SAFE Mode**: Explicitly blocks explicit content
2. **FLIRTY Mode**: Limited to PG-13, no explicit content
3. **NSFW Mode**: 
   - Allows consented adult content
   - **REFUSES**: minors, non-consent, real-person porn, illegal acts
   - Stays within platform policy limits

### User Responsibility

- Users must be 18+ to use NSFW mode (honor system)
- Bot includes safety guardrails in system prompt
- Platform ToS still applies to all modes

---

## FUTURE ENHANCEMENTS

Potential improvements (not implemented):

1. **Age Verification**: Require age confirmation for NSFW mode
2. **Mode-Specific Memory**: Separate conversation history per mode
3. **Custom Modes**: Allow users to create custom system prompts
4. **Mode Scheduling**: Auto-switch modes based on time of day
5. **Content Filtering**: Additional safety layer for NSFW mode
6. **Analytics**: Track mode usage statistics

---

## TROUBLESHOOTING

### Issue: Mode not persisting
**Solution**: Check file permissions on `data/memory/user_modes.json`

### Issue: Keyboard not showing
**Solution**: Ensure `CallbackQueryHandler` is registered in bot.py

### Issue: Mode changes but responses don't reflect it
**Solution**: Check that `get_mode_system_prompt()` is called in `on_text()`

### Issue: File corruption
**Solution**: Atomic writes prevent this. If it happens, delete the file and restart.

---

## SUMMARY

✅ **3 modes implemented**: SAFE, FLIRTY, NSFW  
✅ **Per-user persistence**: JSON file with atomic writes  
✅ **Inline keyboard**: 3 buttons with visual feedback  
✅ **Commands**: /start, /help, /mode updated  
✅ **Typing indicator**: Shows while generating  
✅ **Mode-specific prompts**: Different system prompts per mode  
✅ **All tests passing**: 7/7 tests successful  
✅ **Backward compatible**: Works with existing features  
✅ **Production ready**: Safe defaults, error handling  

**Ready to deploy!** 🚀

