# TicketBooking_webapp

A terminal-style **Flask** mini web app that demonstrates a simple cinema seat booking flow in the browser.

This project is designed to be **embed-friendly** (e.g., in a WordPress site via iframe) and uses **session-based state** to keep the interaction smooth across steps.

# Live Demo
https://datamagic.zoldbolygo.hu/tb


---

## Features

- Movie selection from a predefined list
- Seat map displayed as a **5x5 matrix** (list of lists)
- Ticket count selection
- Seat reservation step-by-step (row + seat)
- Validation:
  - row and seat must be within range (1–5)
  - seat must be available
- “Terminal-like” experience:
  - each step renders a clean screen instead of a scrolling log
  - achieved via session state and phase-based rendering

---

## Tech Stack

- Python 3.x
- Flask 2.3.3

---

## Setup (Local)

1. Create and activate a virtual environment (recommended)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
