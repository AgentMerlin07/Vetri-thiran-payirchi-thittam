# LegalEase — AI-Powered Legal Document Generator

LegalEase implements the supplied project specification using:

- Streamlit frontend
- FastAPI backend
- Gemini AI generation
- Editable document preview
- TXT, DOCX and PDF export
- Pydantic request validation
- Environment-based configuration
- Automated API tests

## Project structure

```text
LegalEase/
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── utils/
│   ├── __init__.py
│   ├── document_formatter.py
│   └── text_utils.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── frontend/
│   └── __init__.py
├── .env.example
├── .gitignore
├── Dockerfile
├── Procfile
├── README.md
├── app.py
├── config.py
├── main.py
├── requirements.txt
├── routes.py
└── schemas.py
```

## Quick Terminal Process (Windows)

For the easiest setup, open a terminal in the `LegalEase` folder and run:

```powershell
.\setup_windows.bat
```

Then use **two terminals**:

**Terminal 1 - Backend**
```powershell
.\run_backend.bat
```

**Terminal 2 - Frontend**
```powershell
.\run_frontend.bat
```

To run automated tests:

```powershell
.\test_backend.bat
```

For the full terminal workflow, troubleshooting, health check, and manual commands, see `terminal_process.md`.

## 1. Requirements

Install Python 3.10 or newer. Python 3.11 is recommended.

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

## 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Gemini

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace:

```text
GEMINI_API_KEY=your_google_gemini_api_key_here
```

with your real Gemini API key.

The source document selected `gemini-1.5-pro`. If Google AI Studio does not make that model available to your account, change only:

```text
GEMINI_MODEL=...
```

to a currently available Gemini model.

Never commit `.env` to Git.

## 4. Start FastAPI

Open Terminal 1:

```powershell
.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Check:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
```

## 5. Start Streamlit

Open Terminal 2:

```powershell
.venv\Scripts\Activate.ps1
streamlit run app.py
```

Streamlit will show the local URL, normally:

```text
http://localhost:8501
```

## 6. Use the application

Enter:

- Document Type
- Parties Involved
- Terms & Conditions
- Effective Date

Use semicolons to separate terms, matching the supplied project specification.

Click **Generate Document**.

Then:

1. Review the preview.
2. Edit the generated text.
3. Download TXT, DOCX, or PDF.

## 7. Test the backend

With dependencies installed:

```powershell
pytest -q
```

The included tests do not call Gemini. They replace the AI generator with a fake generator so the API can be tested without spending API quota.

## 8. Test the real Gemini integration

Start FastAPI and Streamlit, then generate a small document from the UI.

If generation fails, check:

1. `.env` exists.
2. `GEMINI_API_KEY` is correct.
3. `GEMINI_MODEL` is available to your account.
4. Your Google API quota is available.
5. FastAPI is running on port 8000.

## API

### POST `/generate`

Request:

```json
{
  "document_type": "NDA",
  "parties": "Alice (Discloser), Bob (Recipient)",
  "terms": "Confidentiality; 30 day termination",
  "dates": "September 28, 2026"
}
```

Response:

```json
{
  "success": true,
  "document_type": "NDA",
  "content": "..."
}
```

## Legal and safety note

The generated output is an AI-assisted draft. It is not a guarantee of legal validity and should be reviewed for the relevant jurisdiction, facts, and applicable law by an appropriately qualified legal professional before signing or relying on it.

## Deployment

The included `Procfile` and `Dockerfile` provide a starting point for backend deployment. The Streamlit frontend can be deployed separately and configured with the deployed backend URL using `BACKEND_URL`.

For production, replace permissive CORS settings with your actual frontend domain, add authentication/rate limiting, use HTTPS, and avoid logging sensitive document content.
