# 🐶 Dog Grooming Flashcard App

A structured learning application designed to practice dog breed identification and grooming knowledge.

This project demonstrates clean architecture, layered design, and production deployment using Flask.

---

## 🌐 Live Demo

Deployed on:

👉 https://dbfg.zoldbolygo.hu

---

## 🚀 Features

- 🔐 User authentication (hashed passwords)
- 🎴 Adaptive weighted flashcard system
- 📊 Per-card statistics tracking
- 💾 Persistent progress (per user)
- 🧠 CLI and Web interface versions
- 🌿 Clean, minimal UI

---

## 🏗 Architecture Highlights

- Separation between domain logic and UI
- Framework-agnostic game engine
- JSON-based persistence layer
- Flask session-based state management
- Production deployment via cPanel Passenger

---

## 🖥 Interfaces

### Web Version
- Flask
- Jinja2 templates
- Session-based authentication
- Persistent learning progress

### CLI Version
- Terminal-based interaction
- No authentication
- No persistence
- Ideal for debugging and engine testing

---

## 📂 Project Structure

├── app.py # Flask web application
├── cli_DBFG.py # CLI interface
├── game_engine_DBFG.py # Core game logic
├── helpers/
│ ├── auth_utils.py
│ ├── save_manager.py
│ └── path_utils.py
├── templates/
├── static/
├── saves/ # Ignored (runtime files)
└── data_private/ # Ignored (credentials)


---

## 🛠 Tech Stack

- Python 3.9+
- Flask
- Jinja2
- JSON persistence
- Werkzeug security
- cPanel Passenger deployment

---

## 🔒 Security Notes

- Passwords stored as hashed values
- Private user data excluded via `.gitignore`
- Save files stored per user
- Sensitive folders not tracked in Git

---

## 📈 What This Project Demonstrates

- Clean architecture principles
- Layered system design
- State management in web applications
- Production deployment troubleshooting
- Real-world hosting constraints (WordPress + Python coexistence)

---

## 👩‍💻 Author

Edit  
Data, automation and learning  
https://datamagic.zoldbolygo.hu

---
