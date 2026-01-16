# 🔑 Setting Up API Key on Vercel

Your API is deployed at: **https://mcp-iota-seven.vercel.app/**

The `/reason` endpoint is failing because `ANTHROPIC_API_KEY` isn't configured in Vercel yet.

---

## ✅ Current Status (from tests)

**Working endpoints:**
- ✅ `/health` - Returns healthy status
- ✅ `/tools` - Lists all 3 MCP tools
- ✅ `/` - API info endpoint

**Not working:**
- ❌ `/reason` - Returns 500 error (needs API key)

---

## 🔧 How to Set API Key in Vercel

### Step 1: Go to Vercel Dashboard
1. Visit [vercel.com](https://vercel.com)
2. Log in to your account
3. Find your project: `mcp-iota-seven` (or whatever it's named)

### Step 2: Add Environment Variable
1. Click on your project
2. Go to **Settings** tab (left sidebar)
3. Click **Environment Variables** (under Configuration)
4. Click **Add New** button

### Step 3: Configure the Variable
- **Key:** `ANTHROPIC_API_KEY`
- **Value:** Your Anthropic API key (get from [console.anthropic.com](https://console.anthropic.com/))
- **Environment:** Select all environments:
  - ✅ Production
  - ✅ Preview
  - ✅ Development

### Step 4: Redeploy
After adding the environment variable:
1. Go to **Deployments** tab
2. Click the **"..."** menu on the latest deployment
3. Click **Redeploy**
4. Or trigger a new deployment by pushing to GitHub (if connected)

---

## ✅ Verify It Works

After redeploying, test again:

### Quick Test (PowerShell)
```powershell
# Test health (should work)
Invoke-RestMethod -Uri "https://mcp-iota-seven.vercel.app/health"

# Test reason (should work after API key is set)
$body = @{question="Is a verbal promise enforceable?"} | ConvertTo-Json
Invoke-RestMethod -Uri "https://mcp-iota-seven.vercel.app/reason" -Method Post -Body $body -ContentType "application/json"
```

Or use the test script:
```powershell
powershell -ExecutionPolicy Bypass -File test_api.ps1
```

---

## 🔒 Security Notes

- ✅ **Never commit API keys to code** - Always use environment variables
- ✅ **Vercel encrypts environment variables** - Secure storage
- ✅ **Different keys for different environments** - You can use different keys for production/preview

---

## 🎯 What Happens After Setup

Once `ANTHROPIC_API_KEY` is set:
- ✅ `/reason` endpoint will work
- ✅ Full reasoning queries will process
- ✅ All 3 domains (Legal, Health, Science) will function
- ✅ Your API will be fully operational!

---

## 📝 Quick Checklist

- [ ] Get API key from [console.anthropic.com](https://console.anthropic.com/)
- [ ] Add `ANTHROPIC_API_KEY` to Vercel environment variables
- [ ] Redeploy the project
- [ ] Test `/reason` endpoint
- [ ] ✅ API fully working!

---

## ❓ Troubleshooting

**Still getting 500 errors?**
- Check Vercel logs: **Deployments** → Click deployment → **Logs** tab
- Verify API key is correct in Vercel settings
- Make sure you redeployed after adding the variable

**API key not working?**
- Verify key at [console.anthropic.com](https://console.anthropic.com/)
- Check for typos/copy-paste errors
- Ensure key has proper permissions

---

**After setting the API key and redeploying, your API will be fully functional! 🚀**