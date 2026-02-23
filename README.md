# Offline Chatbot (Flask Backend)

An industry-style offline chatbot backend built using Python and Flask.  
This project follows a clean modular architecture with API routes, a service layer, and a storage-ready design that can be extended to support local AI models and persistent memory.

## 🚀 Features

- REST API endpoint for chat: `POST /api/chat`
- Health check endpoint: `GET /api/health`
- Modular backend structure (routes, services, utils, db, models)
- CORS enabled for frontend integration
- Works completely offline
- Easy to extend with:
  - Persistent storage
  - Local AI models (LLMs)
  - Frontend UI
  - Session-based memory

## 📁 Project Structure
offline-chatbot/
├── backend/
│ ├── run.py
│ ├── requirements.txt
│ └── app/
│ ├── init.py
│ ├── routes.py
│ ├── services.py
│ ├── utils.py
│ ├── db.py
│ └── models.py
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
└── README.md


## 🛠️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/harshit-kinger/offline-chatbot.git
cd offline-chatbot

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the server
python run.py

The server will start at:
http://127.0.0.1:5000
📡 API Usage
Chat
POST /api/chat
Content-Type: application/json

{
  "message": "time"
}
Health Check
GET /api/health
🎯 Roadmap

 Finalize persistent storage integration

 Add frontend chat UI

 Integrate local offline AI model

 Add session-based memory

 Improve response logic and knowledge handling

👨‍💻 Author

Harshit Kinger

This project is a learning-focused, industry-style backend showing clean architecture, API design, and extensibility for offline AI systems.


