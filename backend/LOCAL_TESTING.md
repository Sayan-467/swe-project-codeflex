# 🧪 Local Testing Guide

Before deploying to Render, test your services locally to ensure everything works.

---

## 1. Test Auth Service (Node.js)

### Navigate to auth_setup folder
```powershell
cd backend/auth_setup
```

### Install dependencies
```powershell
npm install
```

### Create .env file (if not exists)
```env
PORT=8000
MONGODB_URI=your_mongodb_connection_string
CORS_ORIGIN=*
NODE_ENV=development
```

### Run the service
```powershell
npm run dev
# or
npm start
```

### Test endpoint
Open browser: `http://localhost:8000`
Or use curl:
```powershell
curl http://localhost:8000
```

---

## 2. Test Competitive Services (FastAPI)

### Navigate to backend folder
```powershell
cd backend
```

### Create virtual environment (recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install dependencies
```powershell
pip install -r competitive_services_requirements.txt
```

### Create .env file in backend folder
```env
PORT=8001
GEMINI_API_KEY=your_gemini_api_key
```

### Run the service
```powershell
python competitive_services_main.py
# or
uvicorn competitive_services_main:app --reload --port 8001
```

### Test endpoints
Open browser: `http://localhost:8001`
Interactive docs: `http://localhost:8001/docs`

Test with curl:
```powershell
# Health check
curl http://localhost:8001/

# Test CodeChef hints
curl -X POST http://localhost:8001/codechef/generate/hints `
  -H "Content-Type: application/json" `
  -d '{\"problem_url\": \"https://www.codechef.com/problems/FLOW001\"}'
```

---

## 3. Test Chatbot Services (FastAPI)

### Same backend folder
```powershell
cd backend
```

### Install dependencies (if different from service 2)
```powershell
pip install -r chatbot_services_requirements.txt
```

### Update .env file
```env
PORT=8002
GEMINI_API_KEY=your_gemini_api_key
```

### Run the service
```powershell
python chatbot_services_main.py
# or
uvicorn chatbot_services_main:app --reload --port 8002
```

### Test endpoints
Open browser: `http://localhost:8002`
Interactive docs: `http://localhost:8002/docs`

Test with curl:
```powershell
# Health check
curl http://localhost:8002/

# Test chat
curl -X POST http://localhost:8002/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"What is a binary tree?\"}'

# Test CC editorial
curl "http://localhost:8002/cc_editorial?problem_code=FLOW001&with_hints=true"
```

---

## Common Issues & Solutions

### Issue: Module not found
**Solution**: Make sure you're in the correct directory and have installed dependencies
```powershell
pip install -r requirements.txt
# or
npm install
```

### Issue: Port already in use
**Solution**: Change the PORT in .env or kill the process
```powershell
# Find process on port
netstat -ano | findstr :8000
# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue: MongoDB connection failed
**Solution**: 
- Check if MongoDB URI is correct
- Verify network access is allowed in MongoDB Atlas
- Ensure your IP is whitelisted

### Issue: Import errors in Python
**Solution**: Verify the directory structure matches what's expected
```powershell
# Your backend folder should have:
# - competitive_services_main.py
# - chatbot_services_main.py
# - codechef/ folder
# - codeforces/ folder
# - Chatbot_Backend/ folder
# - CC_Editorial/ folder
```

---

## Running All Services Together

### Terminal 1 - Auth Service
```powershell
cd backend/auth_setup
npm run dev
```

### Terminal 2 - Competitive Services
```powershell
cd backend
python competitive_services_main.py
```

### Terminal 3 - Chatbot Services
```powershell
cd backend
python chatbot_services_main.py
```

Now all three services are running:
- Auth: http://localhost:8000
- Competitive: http://localhost:8001
- Chatbot: http://localhost:8002

---

## Next Steps

Once everything works locally:
1. Commit and push to GitHub
2. Follow DEPLOYMENT_GUIDE.md to deploy on Render
3. Share deployed URLs with frontend team

---

**Happy Testing! 🚀**
