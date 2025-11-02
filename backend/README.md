# 🚀 CodeFlex Backend Services

A microservices-based backend for competitive programming learning platform with AI-powered features.

## 📦 Services Overview

This backend consists of **3 independent microservices**:

1. **Auth Service** - User authentication (Node.js + Express + MongoDB)
2. **Competitive Programming Services** - Editorial scraping & hint generation (Python + FastAPI)
3. **Chatbot Services** - AI chatbot & editorial services (Python + FastAPI)

---

## 🏗️ Architecture

```
Frontend ─┬─► Auth Service (Port 8000)
          ├─► Competitive Services (Port 8001)
          └─► Chatbot Services (Port 8002)
```

---

## 📚 Documentation

- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Complete system architecture and data flow
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Step-by-step Render deployment guide
- **[QUICK_DEPLOY.md](./QUICK_DEPLOY.md)** - Quick reference for deployment
- **[LOCAL_TESTING.md](./LOCAL_TESTING.md)** - Local testing instructions

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd swe-project/backend
```

### 2. Service 1: Auth Service
```bash
cd auth_setup
npm install
# Create .env file with MONGODB_URI
npm start
```

### 3. Service 2: Competitive Services
```bash
cd backend
pip install -r competitive_services_requirements.txt
# Create .env file with GEMINI_API_KEY or OPENAI_API_KEY
python competitive_services_main.py
```

### 4. Service 3: Chatbot Services
```bash
cd backend
pip install -r chatbot_services_requirements.txt
# Create .env file with GEMINI_API_KEY or OPENAI_API_KEY
python chatbot_services_main.py
```

---

## 🌐 API Endpoints

### Auth Service (Port 8000)
- `POST /api/users/register` - Register user
- `POST /api/users/login` - Login user
- `GET /api/users/profile` - Get profile
- `POST /api/notes/create` - Create note
- `GET /api/notes` - Get notes

### Competitive Services (Port 8001)
- `POST /codechef/generate/hints` - Generate CodeChef hints
- `GET /codechef/fetch/editorial` - Fetch CodeChef editorial
- `POST /codeforces/generate/hints` - Generate Codeforces hints
- `GET /codeforces/fetch/editorial` - Fetch Codeforces editorial

### Chatbot Services (Port 8002)
- `POST /chat` - Chat with AI bot
- `GET /cc_editorial` - Get CodeChef editorial with hints

---

## 🔑 Environment Variables

### Auth Service
```env
PORT=8000
MONGODB_URI=your_mongodb_connection_string
NODE_ENV=production
CORS_ORIGIN=*
```

### Python Services
```env
PORT=8001  # or 8002
GEMINI_API_KEY=your_gemini_api_key
# OR
OPENAI_API_KEY=your_openai_api_key
```

---

## 🌍 Deployment (Render)

### Prerequisites
- GitHub account with this repo
- Render account (free tier available)
- MongoDB Atlas account (free tier available)
- Gemini API key (free from Google AI Studio)

### Steps
1. Read **DEPLOYMENT_GUIDE.md** for complete instructions
2. Create 3 web services on Render
3. Configure environment variables
4. Deploy and test

### Expected URLs After Deployment
```
https://codeflex-auth-service.onrender.com
https://codeflex-competitive-services.onrender.com
https://codeflex-chatbot-services.onrender.com
```

---

## 🧪 Testing

### Test Locally
See **LOCAL_TESTING.md** for detailed testing guide.

### Test Deployed Services
```bash
# Health checks
curl https://codeflex-auth-service.onrender.com
curl https://codeflex-competitive-services.onrender.com
curl https://codeflex-chatbot-services.onrender.com

# Interactive API docs (after deployment)
https://codeflex-competitive-services.onrender.com/docs
https://codeflex-chatbot-services.onrender.com/docs
```

---

## 🛠️ Tech Stack

**Service 1 (Auth)**:
- Node.js + Express
- MongoDB + Mongoose
- JWT Authentication
- CORS enabled

**Services 2 & 3 (Python)**:
- FastAPI
- Uvicorn
- Selenium + BeautifulSoup (web scraping)
- Google Generative AI (Gemini)
- OpenAI API (alternative)

---

## 📁 Project Structure

```
backend/
├── auth_setup/              # Node.js auth service
├── codechef/                # CodeChef scraper
├── codeforces/              # Codeforces scraper
├── Chatbot_Backend/         # Chatbot logic
├── CC_Editorial/            # Editorial logic
├── competitive_services_main.py        # Service 2 entry point
├── chatbot_services_main.py            # Service 3 entry point
├── competitive_services_requirements.txt
├── chatbot_services_requirements.txt
└── *.md                     # Documentation files
```

---

## 🤝 Frontend Integration

Share these URLs with your frontend team:

```javascript
const API_BASE_URLS = {
  auth: "https://codeflex-auth-service.onrender.com",
  competitive: "https://codeflex-competitive-services.onrender.com",
  chatbot: "https://codeflex-chatbot-services.onrender.com"
};
```

See **ARCHITECTURE.md** for integration examples.

---

## ⚠️ Important Notes

- Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- MongoDB Atlas requires IP whitelisting (use 0.0.0.0/0 for development)
- Never commit .env files to repository
- Update CORS settings for production

---

## 📝 To-Do

- [ ] Test all services locally
- [ ] Push to GitHub
- [ ] Deploy on Render
- [ ] Update CORS for production
- [ ] Add rate limiting
- [ ] Add request logging
- [ ] Set up monitoring

---

## 🐛 Troubleshooting

See **DEPLOYMENT_GUIDE.md** for common issues and solutions.

---

## 📧 Support

For issues or questions, please check the documentation files or create an issue in the repository.

---

## 📄 License

MIT License

---

**Built with ❤️ for competitive programmers**
