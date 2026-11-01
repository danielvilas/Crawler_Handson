#!/usr/bin/env bash
# Hands-On 03b — Virtual environment & dependencies
# Run these commands from the hands-on/ directory.

# ---- Create the virtual environment ------------------------------------
python -m venv .venv

# ---- Activate (pick your platform) -------------------------------------

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
# .venv\Scripts\activate

# ---- Install dependencies ----------------------------------------------
pip install -r requirements.txt

# ---- Verify all four packages were installed ---------------------------
pip list | grep -E "pymongo|pydantic|fastapi|uvicorn"
