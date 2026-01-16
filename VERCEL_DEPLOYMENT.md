# 🚀 Vercel Deployment Guide

## ✅ Fixed: Routes/Headers Conflict

The error **"If `rewrites`, `redirects`, `headers`, `cleanUrls` or `trailingSlash` are used, then `routes` cannot be present"** has been fixed.

**What changed:**
- Removed `routes` (deprecated in Vercel v2)
- Using `rewrites` instead (modern Vercel approach)
- Kept `headers` for CORS support

---

## 📁 Vercel Deployment Options

### Option 1: Deploy Public Folder Directly (Recommended)

1. **Go to Vercel Dashboard**
2. **New Project** → **Import Git Repository** (or Upload)
3. **Root Directory:** Set to `public` folder
   - Or if deploying whole repo: point root to project root
4. **Build Settings:**
   - Framework Preset: **Other**
   - Build Command: (leave empty for static site)
   - Output Directory: `public` (if deploying from root)
5. **Deploy!**

### Option 2: Use vercel.json (Current Setup)

With the fixed `vercel.json`:
- ✅ No conflicts between `routes` and `headers`
- ✅ Uses `rewrites` to serve from `public/` folder
- ✅ CORS headers enabled for API calls

Just deploy and it should work!

---

## 🔧 vercel.json Explained

```json
{
  "version": 2,
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/public/$1"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    }
  ]
}
```

**What it does:**
- `rewrites`: Maps all requests to the `public/` folder
- `headers`: Adds CORS headers so frontend can call backend API

---

## 📝 Important: Backend API URL

Before deploying, make sure to update the API URL in `public/index.html`:

1. **Deploy your backend** on Render/Railway first
2. **Get your backend URL** (e.g., `https://your-app.onrender.com`)
3. **Edit `public/index.html`:**
   - Find: `<input type="text" id="apiUrl" ... value="http://localhost:8000">`
   - Change to: `value="https://your-app.onrender.com"`
4. **Deploy frontend on Vercel**

---

## 🎯 Deployment Steps

### Step 1: Deploy Backend (Render/Railway)
```bash
# Backend URL: https://your-api.onrender.com
```

### Step 2: Update Frontend API URL
Edit `public/index.html` → Update `apiUrl` input default value

### Step 3: Deploy Frontend (Vercel)
1. Connect GitHub or upload `public/` folder
2. Vercel will use `vercel.json` automatically
3. ✅ Deploy!

### Step 4: Test
- Frontend: `https://your-frontend.vercel.app`
- Should be able to call backend API
- ✅ Demo ready!

---

## 🐛 Troubleshooting

### "Routes cannot be present" Error
- ✅ Fixed! Using `rewrites` instead of `routes`

### "Module not found" Errors
- Vercel is for static sites only
- Backend must be deployed separately (Render/Railway)

### CORS Errors
- `vercel.json` includes CORS headers
- Make sure backend also allows CORS (already configured in `mcp_api_server.py`)

### API URL Not Working
- Check `public/index.html` API URL is correct
- Test backend URL directly: `https://your-api.onrender.com/health`

---

## ✅ Checklist

- [ ] Backend deployed on Render/Railway
- [ ] Backend URL noted down
- [ ] `public/index.html` updated with backend URL
- [ ] `vercel.json` fixed (no `routes`, uses `rewrites`)
- [ ] Deployed on Vercel
- [ ] Tested frontend can call backend

---

**Your Vercel deployment should work now! 🚀**