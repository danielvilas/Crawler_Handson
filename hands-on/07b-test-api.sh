#!/usr/bin/env bash
# Hands-On 07b — Launch the FastAPI server and test the API
# Run these commands from the hands-on/ directory.

# ---- Start the server (keep this running in one terminal) ---------------
uvicorn 07-api:app --reload
# You'll see: Uvicorn running on http://127.0.0.1:8000

# ---- Open the auto-generated docs in your browser -----------------------
# http://localhost:8000/docs       ← Swagger UI (interactive)
# http://localhost:8000/redoc      ← ReDoc (read-friendly)

# ---- curl — list articles (open a second terminal) ----------------------
curl -s "localhost:8000/articles?np_name=elpais"

# With limit parameter
curl -s "localhost:8000/articles?np_name=elpais&limit=20"

# ---- curl — count articles for a newspaper ------------------------------
curl -s "localhost:8000/articles/elpais/count"

# ---- Pretty-print the JSON response -------------------------------------
curl -s "localhost:8000/articles?np_name=elpais" | python -m json.tool
curl -s "localhost:8000/articles/elpais/count"   | python -m json.tool
