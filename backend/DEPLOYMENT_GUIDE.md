# Backend Deployment Guide for Render

## 🚀 Overview
This backend consists of 3 separate services to be deployed on Render:

1. **Auth Service** (Node.js/Express) - Port 8000
2. **Competitive Programming Services** (FastAPI) - Port 8001 (CodeChef + Codeforces)
3. **Chatbot Services** (FastAPI) - Port 8002 (Chatbot + CC_Editorial)

---

## 📦 Service 1: Auth Service (Node.js)

### Repository Setup
- **Root Directory**: `backend/auth_setup`
- **Build Command**: `npm install`
- **Start Command**: `npm start`

### Environment Variables (Add in Render Dashboard)
```
PORT=8000
MONGODB_URI=your_mongodb_connection_string
NODE_ENV=production
```

### Render Configuration
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `codeflex-auth-service`
   - **Root Directory**: `backend/auth_setup`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Instance Type**: Free (or paid as needed)
5. Add environment variables in "Environment" tab
6. Click "Create Web Service"

### Your Service URL
After deployment: `https://codeflex-auth-service.onrender.com`

---

## 📦 Service 2: Competitive Programming Services (FastAPI)

### Repository Setup
- **Root Directory**: `backend`
- **Entry Point**: `competitive_services_main.py`
- **Build Command**: `pip install -r competitive_services_requirements.txt`
- **Start Command**: `uvicorn competitive_services_main:app --host 0.0.0.0 --port $PORT`

### Environment Variables (Add in Render Dashboard)
```
PORT=8001
GEMINI_API_KEY=your_gemini_api_key
# OR
OPENAI_API_KEY=your_openai_api_key
PYTHON_VERSION=3.11.0
```

### Render Configuration
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `codeflex-competitive-services`
   - **Root Directory**: `backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r competitive_services_requirements.txt`
   - **Start Command**: `uvicorn competitive_services_main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or paid as needed)
5. Add environment variables in "Environment" tab
6. Click "Create Web Service"

### Your Service URL
After deployment: `https://codeflex-competitive-services.onrender.com`

### API Endpoints
- `GET /` - Health check
- `POST /codechef/generate/hints` - Generate hints for CodeChef problems
- `GET /codechef/fetch/editorial` - Fetch CodeChef editorial
- `GET /codechef/metadata` - Get CodeChef problem metadata
- `POST /codeforces/generate/hints` - Generate hints for Codeforces problems
- `GET /codeforces/fetch/editorial` - Fetch Codeforces editorial

---

## 📦 Service 3: Chatbot Services (FastAPI)

### Repository Setup
- **Root Directory**: `backend`
- **Entry Point**: `chatbot_services_main.py`
- **Build Command**: `pip install -r chatbot_services_requirements.txt`
- **Start Command**: `uvicorn chatbot_services_main:app --host 0.0.0.0 --port $PORT`

### Environment Variables (Add in Render Dashboard)
```
PORT=8002
GEMINI_API_KEY=your_gemini_api_key
# OR
OPENAI_API_KEY=your_openai_api_key
PYTHON_VERSION=3.11.0
```

### Render Configuration
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `codeflex-chatbot-services`
   - **Root Directory**: `backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r chatbot_services_requirements.txt`
   - **Start Command**: `uvicorn chatbot_services_main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or paid as needed)
5. Add environment variables in "Environment" tab
6. Click "Create Web Service"

### Your Service URL
After deployment: `https://codeflex-chatbot-services.onrender.com`

### API Endpoints
- `GET /` - Health check
- `POST /chat` - AI chatbot for programming queries
- `GET /cc_editorial?problem_code=FLOW001&with_hints=true` - Get CodeChef editorial with hints

---

## 🔧 Important Notes

### For Selenium-based Services (Web Scraping)
If you face issues with Chrome/ChromeDriver on Render, you may need to:

1. Add a `render.yaml` file (optional) or use Render's build commands
2. Install Chrome dependencies in build command:
```bash
apt-get update && apt-get install -y wget gnupg && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && apt-get update && apt-get install -y google-chrome-stable && pip install -r requirements.txt
```

**Simpler approach**: Use `requests` and `BeautifulSoup` for scraping instead of Selenium where possible.

### Free Tier Limitations
- Free services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Consider using paid plans for production

### CORS Configuration
All services are configured with `allow_origins=["*"]` for development.
**For production**, update this in each main file:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 Testing Your Deployed Services

### Test Auth Service
```bash
curl https://codeflex-auth-service.onrender.com/
```

### Test Competitive Services
```bash
# Health check
curl https://codeflex-competitive-services.onrender.com/

# Generate hints for CodeChef
curl -X POST https://codeflex-competitive-services.onrender.com/codechef/generate/hints \
  -H "Content-Type: application/json" \
  -d '{"problem_url": "https://www.codechef.com/problems/FLOW001"}'
```

### Test Chatbot Services
```bash
# Health check
curl https://codeflex-chatbot-services.onrender.com/

# Chat
curl -X POST https://codeflex-chatbot-services.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a linked list?"}'
```

---

## 🔗 Frontend Integration

Share these URLs with your frontend team:

```javascript
const API_ENDPOINTS = {
  auth: "https://codeflex-auth-service.onrender.com",
  competitive: "https://codeflex-competitive-services.onrender.com",
  chatbot: "https://codeflex-chatbot-services.onrender.com"
};
```

---

## 🐛 Troubleshooting

### Service won't start
- Check logs in Render dashboard
- Verify environment variables are set correctly
- Ensure build command completed successfully

### MongoDB connection issues
- Whitelist `0.0.0.0/0` in MongoDB Atlas Network Access
- Verify connection string format
- Check if MongoDB password contains special characters (URL encode them)

### Import errors
- Ensure all dependencies are in requirements.txt
- Check Python version compatibility
- Verify root directory is set correctly

### 502 Bad Gateway
- Service is likely spinning up (wait 30-60 seconds)
- Check if port binding is correct (`0.0.0.0`)
- Verify start command syntax

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Node.js on Render](https://render.com/docs/deploy-node-express-app)

---

## ✅ Deployment Checklist

- [ ] Push all code to GitHub
- [ ] Create MongoDB Atlas cluster (if using MongoDB)
- [ ] Get API keys (Gemini/OpenAI)
- [ ] Create Auth Service on Render
- [ ] Create Competitive Services on Render
- [ ] Create Chatbot Services on Render
- [ ] Add environment variables to all services
- [ ] Test all endpoints
- [ ] Share URLs with frontend team
- [ ] Update CORS settings for production

---

**Good luck with your deployment! 🚀**
