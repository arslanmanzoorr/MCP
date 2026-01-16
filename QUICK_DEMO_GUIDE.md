# ⚡ Quick Demo Guide - Show Client in 5 Minutes

You want to demo this **TODAY** but can't deploy on Vercel? Here's the fastest way!

---

## 🚀 Option 1: Local Demo with Beautiful UI (5 minutes)

### Windows:
```bash
# 1. Set API key
$env:ANTHROPIC_API_KEY = "your_key_here"

# 2. Run the quick demo script
quick_demo.bat
```

### Mac/Linux:
```bash
# 1. Set API key
export ANTHROPIC_API_KEY="your_key_here"

# 2. Make script executable and run
chmod +x quick_demo.sh
./quick_demo.sh
```

**What happens:**
- ✅ API server starts on `http://localhost:8000`
- ✅ Beautiful demo interface opens in browser
- ✅ You can ask questions immediately!

---

## 🌐 Option 2: Public Demo with ngrok (10 minutes)

### Step 1: Install ngrok
- Download: https://ngrok.com/download
- Extract `ngrok.exe` (Windows) or `ngrok` (Mac/Linux)

### Step 2: Start API Server
```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "your_key_here"
python mcp_api_server.py
```

### Step 3: Expose with ngrok (in new terminal)
```bash
ngrok http 8000
```

You'll get a public URL like: `https://abc123.ngrok.io`

### Step 4: Update Frontend
1. Open `public/index.html` in a text editor
2. Find line with: `value="http://localhost:8000"`
3. Change to: `value="https://abc123.ngrok.io"` (your ngrok URL)
4. Save and open `public/index.html` in browser

**Now you have a public URL you can share with your client!**

---

## 🎨 Option 3: Deploy Frontend on Vercel + Backend on Render (30 minutes)

This is the **most professional** option:

### Backend (Render.com - 15 minutes)

1. **Sign up** at [render.com](https://render.com) (free)

2. **Create Web Service**
   - Connect GitHub repo or upload code
   - Settings:
     ```
     Build: pip install -r requirements.txt
     Start: python mcp_api_server.py
     ```
   - Add environment variable: `ANTHROPIC_API_KEY`

3. **Deploy** → Get URL: `https://your-app.onrender.com`

### Frontend (Vercel - 5 minutes)

1. **Create account** at [vercel.com](https://vercel.com)

2. **New Project**
   - Upload `public/` folder OR
   - Connect GitHub and point to `public/` directory

3. **Before deploying**, edit `public/index.html`:
   - Change default API URL to your Render URL
   - Line: `value="https://your-app.onrender.com"`

4. **Deploy** → Get URL: `https://your-demo.vercel.app`

**✅ Professional demo with separate frontend/backend!**

---

## 🎯 What Each Option Gives You

| Option | Time | Public URL? | Best For |
|--------|------|-------------|----------|
| **Local Demo** | 5 min | ❌ No | Immediate demo, same computer |
| **ngrok** | 10 min | ✅ Yes | Demo TODAY, share URL |
| **Render + Vercel** | 30 min | ✅ Yes | Professional, permanent demo |

---

## 💡 Pro Tips

### For Client Presentation:

1. **Use Option 2 (ngrok)** if you need it TODAY
   - Client can access from their computer
   - Looks professional (HTTPS URL)
   - Free and takes 10 minutes

2. **Use Option 3 (Render + Vercel)** for permanent demo
   - Most professional setup
   - Client can access anytime
   - Easy to share with stakeholders

3. **Use Option 1 (Local)** for quick testing
   - Fastest way to test
   - Good for preparation

### During Demo:

- **Show the Swagger UI**: `http://your-url/docs` (impressive!)
- **Use the quick questions** in the demo interface
- **Show all 3 domains**: Legal, Health, Science
- **Highlight the structured output** and validation

---

## 🛠️ Troubleshooting

### "API key not set" error
```bash
# Windows
$env:ANTHROPIC_API_KEY = "your_key_here"

# Mac/Linux
export ANTHROPIC_API_KEY="your_key_here"
```

### "Port 8000 already in use"
```bash
# Change port
$env:MCP_PORT = "8001"  # Windows
export MCP_PORT=8001    # Mac/Linux

# Then update ngrok or frontend URL
ngrok http 8001
```

### "Module not found" error
```bash
pip install -r requirements.txt
```

---

## 📋 Pre-Demo Checklist

- [ ] API key is set
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Tested locally (run `quick_demo.bat` or `quick_demo.sh`)
- [ ] Have 3 demo questions ready:
  - Legal: "Is a verbal promise enforceable?"
  - Health: "What could explain chest discomfort?"
  - Science: "Can temperature explain reaction rates?"
- [ ] Opened `public/index.html` to verify UI works

---

## ✅ You're Ready!

**Recommended path:**
1. **NOW**: Use ngrok (10 min) → Get public URL
2. **LATER**: Deploy on Render + Vercel (30 min) → Professional permanent demo

**Good luck with your demo! 🚀**