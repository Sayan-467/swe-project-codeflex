# 📊 Backend Architecture Overview

## System Architecture

```
                         ┌─────────────────────────────┐
                         │      FRONTEND (React)       │
                         │   Your Teammate's Work      │
                         └──────────────┬──────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
        ┌───────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │   Auth Service    │ │  Competitive    │ │    Chatbot      │
        │    (Node.js)      │ │   Programming   │ │    Services     │
        │   Express + JWT   │ │    (FastAPI)    │ │    (FastAPI)    │
        │                   │ │                 │ │                 │
        │  Port: 8000       │ │  Port: 8001     │ │  Port: 8002     │
        └─────────┬─────────┘ └────────┬────────┘ └────────┬────────┘
                  │                    │                    │
                  │                    │                    │
                  ▼                    ▼                    ▼
        ┌─────────────────┐  ┌─────────────────┐ ┌─────────────────┐
        │   MongoDB       │  │  Web Scraping   │ │   AI/LLM APIs   │
        │   Database      │  │  CodeChef, CF   │ │  Gemini/OpenAI  │
        └─────────────────┘  └─────────────────┘ └─────────────────┘
```

---

## Service Details

### 🔐 Service 1: Auth Service
**Technology**: Node.js + Express
**Port**: 8000
**Purpose**: User authentication and management

**Features**:
- User registration
- User login/logout
- JWT token management
- Protected routes
- MongoDB integration

**API Endpoints**:
```
POST   /api/users/register    - Register new user
POST   /api/users/login       - Login user
GET    /api/users/profile     - Get user profile
PUT    /api/users/update      - Update user info
POST   /api/notes/create      - Create note
GET    /api/notes             - Get all notes
```

**Dependencies**:
- express
- mongoose
- cors
- dotenv

---

### 🏆 Service 2: Competitive Programming Services
**Technology**: Python + FastAPI
**Port**: 8001
**Purpose**: Editorial scraping and hint generation for competitive programming

**Features**:
- CodeChef problem editorial scraping
- Codeforces problem editorial scraping
- AI-powered hint generation
- Problem metadata extraction

**API Endpoints**:
```
GET    /                                  - Health check
POST   /codechef/generate/hints          - Generate hints for CodeChef
GET    /codechef/fetch/editorial         - Fetch CodeChef editorial
GET    /codechef/metadata                - Get problem metadata
POST   /codeforces/generate/hints        - Generate hints for Codeforces
GET    /codeforces/fetch/editorial       - Fetch Codeforces editorial
```

**Request Example**:
```json
POST /codechef/generate/hints
{
  "problem_url": "https://www.codechef.com/problems/FLOW001"
}
```

**Response Example**:
```json
{
  "problem": {
    "problem_code": "FLOW001",
    "name": "Add Two Numbers",
    "editorial_url": "..."
  },
  "generated_hints": "Hint 1: ...\nHint 2: ...",
  "platform": "CodeChef"
}
```

**Dependencies**:
- fastapi
- uvicorn
- selenium
- beautifulsoup4
- requests
- google-generativeai / openai

---

### 🤖 Service 3: Chatbot Services
**Technology**: Python + FastAPI
**Port**: 8002
**Purpose**: AI chatbot and CodeChef editorial with hints

**Features**:
- AI-powered programming chatbot
- Context-aware conversations
- CodeChef editorial with hint generation
- Real-time responses

**API Endpoints**:
```
GET    /                        - Health check
POST   /chat                    - Chat with AI bot
GET    /cc_editorial            - Get CodeChef editorial with hints
```

**Request Example**:
```json
POST /chat
{
  "message": "Explain binary search",
  "context": ["previous", "messages", "optional"]
}
```

**Response Example**:
```json
{
  "reply": "Binary search is a divide and conquer algorithm...",
  "service": "chatbot"
}
```

**Dependencies**:
- fastapi
- uvicorn
- google-generativeai
- python-dotenv

---

## Data Flow

### User Authentication Flow
```
Frontend → Auth Service → MongoDB → Auth Service → Frontend
                                      (JWT Token)
```

### Problem Hint Generation Flow
```
Frontend → Competitive Service → Web Scraper → Editorial Text
                ↓
         AI API (Gemini/OpenAI) → Generated Hints
                ↓
            Frontend
```

### Chatbot Flow
```
Frontend → Chatbot Service → AI API → Response → Frontend
```

---

## Environment Variables

### Auth Service (.env)
```env
PORT=8000
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
NODE_ENV=production
CORS_ORIGIN=*
```

### Competitive Services (.env)
```env
PORT=8001
GEMINI_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here
```

### Chatbot Services (.env)
```env
PORT=8002
GEMINI_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here
```

---

## Deployment URLs (After Render Deployment)

```
Auth Service:        https://codeflex-auth-service.onrender.com
Competitive Service: https://codeflex-competitive-services.onrender.com
Chatbot Service:     https://codeflex-chatbot-services.onrender.com
```

---

## Frontend Integration Example

```javascript
// config/api.js
export const API_CONFIG = {
  auth: {
    baseURL: 'https://codeflex-auth-service.onrender.com',
    endpoints: {
      register: '/api/users/register',
      login: '/api/users/login',
      profile: '/api/users/profile',
    }
  },
  competitive: {
    baseURL: 'https://codeflex-competitive-services.onrender.com',
    endpoints: {
      codechefHints: '/codechef/generate/hints',
      codeforcesHints: '/codeforces/generate/hints',
      codechefEditorial: '/codechef/fetch/editorial',
    }
  },
  chatbot: {
    baseURL: 'https://codeflex-chatbot-services.onrender.com',
    endpoints: {
      chat: '/chat',
      ccEditorial: '/cc_editorial',
    }
  }
};

// Usage example
import axios from 'axios';
import { API_CONFIG } from './config/api';

// Login user
const login = async (email, password) => {
  const response = await axios.post(
    `${API_CONFIG.auth.baseURL}${API_CONFIG.auth.endpoints.login}`,
    { email, password }
  );
  return response.data;
};

// Get hints for problem
const getHints = async (problemUrl, platform = 'codechef') => {
  const endpoint = platform === 'codechef' 
    ? API_CONFIG.competitive.endpoints.codechefHints
    : API_CONFIG.competitive.endpoints.codeforcesHints;
    
  const response = await axios.post(
    `${API_CONFIG.competitive.baseURL}${endpoint}`,
    { problem_url: problemUrl }
  );
  return response.data;
};

// Chat with bot
const chat = async (message, context = null) => {
  const response = await axios.post(
    `${API_CONFIG.chatbot.baseURL}${API_CONFIG.chatbot.endpoints.chat}`,
    { message, context }
  );
  return response.data;
};
```

---

## Files Structure After Setup

```
backend/
├── auth_setup/                          # Service 1 files
│   ├── src/
│   ├── public/
│   ├── app.js                           ✅ Modified
│   ├── index.js                         ✅ Modified
│   ├── package.json
│   └── .env                             (create this)
│
├── codechef/                            # CodeChef scraper
│   ├── cc_editorial.py
│   └── ...
│
├── codeforces/                          # Codeforces scraper
│   ├── cf_editorial.py
│   └── ...
│
├── Chatbot_Backend/                     # Chatbot logic
│   ├── chatbot_core.py
│   └── ...
│
├── CC_Editorial/                        # CC editorial logic
│   ├── cc_editorial.py
│   ├── hint_generator.py
│   └── ...
│
├── competitive_services_main.py         ✅ NEW - Service 2 entry
├── competitive_services_requirements.txt ✅ NEW - Service 2 deps
├── chatbot_services_main.py             ✅ NEW - Service 3 entry
├── chatbot_services_requirements.txt    ✅ NEW - Service 3 deps
├── DEPLOYMENT_GUIDE.md                  ✅ NEW - Full guide
├── QUICK_DEPLOY.md                      ✅ NEW - Quick reference
├── LOCAL_TESTING.md                     ✅ NEW - Testing guide
└── ARCHITECTURE.md                      ✅ NEW - This file
```

---

## Key Features Summary

✅ **Scalable Architecture**: 3 independent microservices
✅ **Modern Tech Stack**: Node.js + Python (FastAPI)
✅ **AI Integration**: Gemini/OpenAI for hint generation
✅ **Web Scraping**: Selenium + BeautifulSoup for editorials
✅ **Authentication**: JWT-based secure auth
✅ **CORS Enabled**: Ready for frontend integration
✅ **Cloud Ready**: Configured for Render deployment
✅ **Free Tier Compatible**: Works with free hosting
✅ **Well Documented**: Complete guides included

---

## Next Steps

1. ✅ Review this architecture
2. ✅ Test locally (see LOCAL_TESTING.md)
3. ✅ Push to GitHub
4. ✅ Deploy on Render (see DEPLOYMENT_GUIDE.md)
5. ✅ Share URLs with frontend team
6. ✅ Integrate with frontend

---

**Your backend is ready to deploy! 🚀**
