# Architecture – Dog Grooming Flashcard System

## Overview

This project follows a layered architecture that separates:

- Domain logic
- Persistence
- Authentication
- Interface layers (CLI & Web)

The system is intentionally framework-agnostic at its core.

---

## High-Level Architecture

JSON Data (dogs.json)
↓
Game Engine (game_engine_DBFG.py)
↓
Persistence Layer (helpers/save_manager.py)
↓
Interface Layer
├── CLI (cli_DBFG.py)
└── Web (app.py + templates)


---

## Core Layers

### 1. Domain Layer (Game Engine)

File: `game_engine_DBFG.py`

Responsibilities:

- Card loading
- Adaptive weighted random selection
- Answer normalization & comparison
- Statistics tracking
- Learning progression
- State export/import

The engine:

- Contains no UI logic
- Contains no authentication logic
- Contains no file-saving logic
- Is reusable by both CLI and Flask interfaces

This ensures clean separation of concerns.

---

### 2. Persistence Layer

File: `helpers/save_manager.py`

Responsibilities:

- Store user progress as JSON
- Load saved game state
- Delete saved state (reset)

Design choice:
Game engine never writes files directly.
Persistence is external and injectable.

---

### 3. Authentication Layer

File: `helpers/auth_utils.py`

Responsibilities:

- Validate user credentials
- Verify password hash
- Check access expiration

Passwords are stored as hashed values in:
`data_private/users.json`

---

### 4. Interface Layers

#### CLI Interface
File: `cli_DBFG.py`

- Pure terminal interaction
- No persistence
- No authentication
- Ideal for debugging engine logic

#### Web Interface
File: `app.py`

- Flask-based
- Session handling
- Persistent state per user
- Jinja templates for rendering

---

## State Management Strategy

Web version:

- Current user stored in Flask session
- Current card ID stored in session
- Full engine state stored in:
  `saves/<username>.json`

CLI version:

- State only exists in memory

---

## Deployment Architecture

Production environment:

- Hosted via cPanel Python App
- Served through Passenger WSGI
- Deployed on subdomain:
  `dbfg.zoldbolygo.hu`

Important deployment decisions:

- Separate subdomain from WordPress
- Dedicated application root
- Virtual environment managed by cPanel
- Static files served through Flask

---

## Design Principles

- Separation of concerns
- Framework-independent domain layer
- Stateless HTTP routes
- JSON-based persistence
- Minimal external dependencies
- Clean layered architecture

---

## Future Extension Possibilities

- Multiple card packs
- Spaced repetition algorithm
- API layer (REST)
- Admin dashboard
- User roles
- Analytics export

---

## Summary

The project demonstrates:

- Clean architecture
- Multi-interface design (CLI + Web)
- Stateful web sessions
- JSON persistence strategy
- Production deployment experience
