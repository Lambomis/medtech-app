# 🧠 MedTech App

This project provides a modular architecture for a **medical image processing app**, split into two independent services:

- **Backend** (FastAPI): Handles image uploads and processing.  
- **Frontend** (Vanilla JS + HTML/CSS): Provides a simple UI to interact with the backend.  
- **Main Launcher** (`main.py`): Runs both services locally for testing or development.

---

## 🚀 Features

- Modular structure: separate `frontend` and `backend` modules under `modules/`.
- Automatic configuration handling via `config.json`.
- Local testing with both servers running simultaneously.
- Safe shutdown via `CTRL+C`.
- Dynamic frontend–backend connection setup.

---

## 🗂️ Project Structure
```bash
project_root/
│
├── main.py # Runs backend & frontend together (local testing)
├── config.json # Configuration file (auto-generated on first run)
├── modules/
│ ├── backend/
│ │ └── app.py # FastAPI backend logic
│ └── frontend/
│ ├── index.html # Frontend entry point
│ ├── style.css # UI styling
│ ├── scripts.js # Frontend logic
│ └── config.js # Auto-generated (backend URL)
└── README.md
```
---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create and activate venv
```bash
python -m venv .venv
source .venv/bin/activate    # On Linux/Mac
.venv\Scripts\activate       # On Windows
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Run Locally
```bash
python main.py
```