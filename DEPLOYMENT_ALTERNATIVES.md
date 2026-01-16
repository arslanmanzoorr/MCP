# 🚀 Deployment Alternatives for Client Demo

Since Vercel is designed for static sites and serverless functions (not long-running Python apps), here are **better alternatives** that work perfectly for FastAPI applications.

---

## 🎯 **Recommended: Render.com** (Easiest & Free)

**Why Render?**
- ✅ Free tier available
- ✅ Python/FastAPI support out of the box
- ✅ Simple deployment (connect GitHub)
- ✅ Automatic HTTPS
- ✅ Environment variables support
- ✅ Takes ~5 minutes to deploy

### Step 1: Prepare Your Code

Make sure you have a `requirements.txt` file (you already do!)

### Step 2: Deploy on Render

1. **Sign up** at [render.com](https://render.com) (free account)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository (or upload zip)

3. **Configure Service**
   ```
   Name: mcp-reasoning-engine
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python mcp_api_server.py
   ```

4. **Set Environment Variable**
   - Go to "Environment" tab
   - Add: `ANTHROPIC_API_KEY` = `your_api_key_here`

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Your API will be live at: `https://mcp-reasoning-engine.onrender.com`

### Step 3: Update Frontend

Deploy the `public/index.html` file on Vercel, and set the API URL to your Render URL!

---

## 🚂 **Alternative: Railway.app** (Also Easy & Free)

**Why Railway?**
- ✅ Free tier ($5 credit/month)
- ✅ Very simple deployment
- ✅ One-click deploy from GitHub
- ✅ Automatic HTTPS

### Deploy on Railway

1. **Sign up** at [railway.app](https://railway.app)

2. **New Project** → "Deploy from GitHub repo"

3. **Configure**
   - Railway auto-detects Python
   - Add environment variable: `ANTHROPIC_API_KEY`

4. **Deploy!**
   - Railway automatically detects your `mcp_api_server.py`
   - Your API will be live at: `https://your-app.up.railway.app`

---

## 🪁 **Alternative: Fly.io** (Free Tier Available)

**Why Fly.io?**
- ✅ Free tier (3 shared VMs)
- ✅ Global edge network
- ✅ Good for demo/production

### Quick Deploy on Fly.io

1. **Install flyctl**:
   ```bash
   # Windows PowerShell
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Create `fly.toml`** (I'll create this for you)

3. **Deploy**:
   ```bash
   fly auth login
   fly launch
   fly secrets set ANTHROPIC_API_KEY=your_key_here
   fly deploy
   ```

---

## 💻 **Option: Local Demo + ngrok** (For Immediate Demo)

**Best for:** Showing client TODAY without deploying

### Step 1: Run Locally
```bash
python mcp_api_server.py
```

### Step 2: Expose with ngrok
```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000
```

This gives you a public URL like: `https://abc123.ngrok.io`

### Step 3: Update Frontend
Use the ngrok URL in your `public/index.html`

---

## 🌐 **Hybrid: Vercel Frontend + Backend Elsewhere**

This is the **BEST approach** for your situation:

### Backend → Render/Railway
- Deploy `mcp_api_server.py` on Render or Railway
- Get backend URL: `https://your-api.onrender.com`

### Frontend → Vercel
- Deploy the `public/index.html` file on Vercel
- Update API URL in the HTML to point to your backend
- Client sees beautiful UI on Vercel!

---

## 📝 Quick Deployment Script

I'll create a deployment helper script that you can use:

---

## ✅ **Recommended Path for Your Client Demo**

**Option 1: Fastest (30 minutes)**
1. Deploy backend on Render (free, 5 min setup)
2. Deploy frontend HTML on Vercel (2 min)
3. Connect them together
4. ✅ Demo ready!

**Option 2: Immediate (5 minutes)**
1. Run `python mcp_api_server.py` locally
2. Run `ngrok http 8000` to expose it
3. Update `public/index.html` with ngrok URL
4. Open the HTML file locally
5. ✅ Demo ready NOW!

---

## 🔧 What I've Created For You

1. **`public/index.html`** - Beautiful demo frontend (deploy on Vercel)
2. **`DEPLOYMENT_ALTERNATIVES.md`** - This guide
3. Deployment configs (coming next)

---

## 🚀 Next Steps

Choose your path:
- **Need it NOW?** → Use ngrok (5 minutes)
- **Have 30 minutes?** → Deploy on Render (most professional)
- **Want simplest?** → Use Railway (one-click deploy)

Let me know which option you prefer, and I'll create the specific deployment files!