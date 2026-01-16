# 🔗 How This Works with Claude

## Understanding the Setup

Your API **already uses Claude AI** internally! Here's how it works:

```
Your API (Vercel) 
    ↓
Uses Anthropic API 
    ↓
Calls Claude AI 
    ↓
Returns reasoning results
```

---

## ⚠️ Important: You Need API Key

Your API (`/reason` endpoint) needs `ANTHROPIC_API_KEY` to work because:

1. **User sends question** → Your API receives it
2. **Your API calls Claude** → Uses Anthropic API (needs API key)
3. **Claude processes** → Uses MCP tools (search, validate, evaluate)
4. **Returns result** → Structured reasoning output

**Without the API key:** Step 2 fails → 500 error

---

## ✅ Two Ways to Use Claude

### Option 1: Your API Uses Claude (Current Setup) ⭐

**How it works:**
- User → Your API → Claude AI → Response
- Your API needs `ANTHROPIC_API_KEY` in Vercel

**What you need:**
- Set `ANTHROPIC_API_KEY` in Vercel environment variables
- Your API will automatically use Claude

**Best for:**
- ✅ Production deployment
- ✅ Client-facing demo
- ✅ Permanent API

---

### Option 2: Claude Calls Your API (Alternative)

**How it works:**
- You → Claude Chat → Your API → Response
- Claude can make HTTP requests to your API

**What you need:**
- Your API deployed (✅ already done!)
- Claude can access the internet
- You give Claude the API URL

**Best for:**
- Testing your API
- Interactive exploration
- Quick demos

**Example with Claude Chat:**
```
You: "Call this API: https://mcp-iota-seven.vercel.app/reason
     with question: 'Is a verbal promise enforceable?'"

Claude: [Makes POST request and returns the result]
```

---

## 🎯 What You Need to Do

### To Make Your API Work with Claude:

1. **Get Anthropic API Key**
   - Go to [console.anthropic.com](https://console.anthropic.com/)
   - Create/get your API key

2. **Add to Vercel**
   - Vercel Dashboard → Your Project → Settings
   - Environment Variables → Add `ANTHROPIC_API_KEY`
   - Redeploy

3. **Test It**
   - Your API will now use Claude internally
   - `/reason` endpoint will work

---

## 💡 Using Claude Chat to Test Your API

You can also ask Claude (this chat assistant) to test your API:

```
You: "Can you test this API endpoint?
     POST https://mcp-iota-seven.vercel.app/reason
     Body: {'question': 'Is a verbal promise enforceable?'}"
```

Claude can make the HTTP request and show you the results!

---

## 🔄 Summary

| Setup | What Happens | API Key Needed? |
|-------|--------------|-----------------|
| **Your API → Claude** | API uses Claude internally | ✅ Yes (in Vercel) |
| **Claude → Your API** | Claude calls your API | ❌ No (API is public) |

**Current Status:**
- ✅ Your API is deployed
- ❌ API key not set in Vercel
- ⚠️ `/reason` endpoint needs API key to use Claude

**To Fix:**
- Add `ANTHROPIC_API_KEY` to Vercel → Redeploy → ✅ Works!

---

## 🚀 Next Steps

1. **Get API key** from Anthropic
2. **Add to Vercel** environment variables  
3. **Redeploy**
4. **Test** - Your API will use Claude successfully!

---

**Bottom line:** Your API is already designed to use Claude! You just need to add the API key to Vercel so it can authenticate with Anthropic. 🔑