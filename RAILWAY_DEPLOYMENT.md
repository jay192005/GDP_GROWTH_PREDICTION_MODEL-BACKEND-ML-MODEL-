# Deploy Backend to Railway

## Why Railway Instead of Vercel?

Vercel has significant limitations for Python backends:
- ❌ 50MB deployment size limit (your model is 57MB)
- ❌ 10-second execution timeout
- ❌ Limited Python support

Railway is perfect for your backend:
- ✅ No file size limits
- ✅ Full Python support
- ✅ Easy deployment
- ✅ $5 free credit/month
- ✅ No sleep (unlike Heroku free tier)

## Step-by-Step Deployment

### 1. Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### 2. Deploy Your Backend

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose: `GDP_GROWTH_PREDICTION_MODEL-BACKEND-ML-MODEL-`
4. Railway will automatically:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Start your Flask app
5. Wait 2-3 minutes for deployment

### 3. Get Your Backend URL

1. Click on your deployed service
2. Go to "Settings" tab
3. Scroll to "Domains" section
4. Click "Generate Domain"
5. Copy the URL (e.g., `https://your-app.up.railway.app`)

### 4. Update Frontend Environment Variable

Now update your Vercel frontend:

1. Go to [vercel.com](https://vercel.com)
2. Open your frontend project
3. Go to "Settings" → "Environment Variables"
4. Edit `VITE_API_BASE_URL`
5. Set value to your Railway URL: `https://your-app.up.railway.app`
6. Click "Save"
7. Go to "Deployments" → Click "..." → "Redeploy"

### 5. Update Backend CORS

After getting your Vercel frontend URL, update CORS in your backend:

1. Go to your backend repository on GitHub
2. Edit `app.py`
3. Update the CORS line:

```python
CORS(app, origins=[
    "http://localhost:5173",
    "https://your-frontend.vercel.app"  # Add your Vercel URL
])
```

4. Commit and push
5. Railway will auto-redeploy

## Testing Your Deployment

### Test Backend API

```bash
# Health check
curl https://your-app.up.railway.app/

# Get countries
curl https://your-app.up.railway.app/api/countries

# Get history
curl "https://your-app.up.railway.app/api/history?country=United%20States"
```

### Test Frontend

1. Open your Vercel URL
2. Select a country
3. Check if historical data loads
4. Test prediction feature

## Troubleshooting

### Backend Not Starting
- Check Railway logs: Click on your service → "Deployments" → Click latest deployment → "View Logs"
- Verify `requirements.txt` has all dependencies
- Check if `PORT` environment variable is being used

### CORS Errors
- Make sure you added your Vercel URL to CORS origins
- Push changes to GitHub (Railway auto-redeploys)
- Clear browser cache

### Model Not Loading
- Check Railway logs for "Model and Encoder loaded" message
- Verify `gdp_model.pkl` and `country_encoder.pkl` are in repository
- Check file sizes in Railway dashboard

## Cost

Railway Free Tier:
- $5 free credit per month
- ~500 hours of usage
- Perfect for development and small projects

## Alternative: Render

If you prefer Render over Railway:

1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Deploy

Render also has a free tier with 750 hours/month.

## Files Added for Deployment

- `runtime.txt` - Specifies Python version
- `Procfile` - Tells Railway how to start the app
- `app.py` - Updated to use PORT environment variable

---

**Need Help?**
- Railway Docs: https://docs.railway.app/
- Railway Discord: https://discord.gg/railway
