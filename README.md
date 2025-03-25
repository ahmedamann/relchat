# RelChat - AI-Powered Chat Application (The app is still a work in progress and is not finished)

RelChat is a full-stack chat application powered by a React frontend, FastAPI backend, and Ollama for AI language model interactions. It uses Retrieval-Augmented Generation (RAG) for document uploads to enhance responses based on the content of uploaded files.

## 🛠️ **Tech Stack**
- **Frontend:** React (Vite)
- **Backend:** FastAPI
- **AI Model:** Ollama (LLaMA 3.2)
- **Database:** SQLite
- **Containerization:** Docker & Docker Compose

---

## 🚀 **Getting Started**

### Clone the Repository
```bash
git clone https://github.com/your-repo/relchat.git
cd relchat
```

### Build and Run
```bash
docker-compose up -d
```
This will start:
- FastAPI on `http://localhost:8000`
- React Frontend on `http://localhost:5173`
- Ollama on `http://localhost:11434`

## 📁 **Project Structure**
```bash
relchat/
├── react-frontend/       # Frontend application
├── fastapi-backend/      # Backend API
├── ollama/               # AI Model setup
├── docker-compose.yml    # Docker configuration
└── README.md             # Project guide
```

