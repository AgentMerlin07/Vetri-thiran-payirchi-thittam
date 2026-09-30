# LegalEase - Terminal Process

This file shows the complete Windows terminal workflow for running LegalEase.

## 1. Open the project

```powershell
cd "path\to\LegalEase"
```

## 2. Create the virtual environment

Run once:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Gemini

```powershell
Copy-Item .env.example .env
```

Open `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL=YOUR_AVAILABLE_GEMINI_MODEL
```

Do not share or commit the `.env` file.

## 5. Run backend - Terminal 1

```powershell
cd "path\to\LegalEase"
.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

Keep Terminal 1 running.

## 6. Run frontend - Terminal 2

Open a second terminal:

```powershell
cd "path\to\LegalEase"
.venv\Scripts\Activate.ps1
streamlit run app.py
```

Frontend:

```text
http://localhost:8501
```

Keep Terminal 2 running.

## 7. Test the backend

Open a third terminal:

```powershell
cd "path\to\LegalEase"
.venv\Scripts\Activate.ps1
pytest -q
```

The automated tests use a fake generator and do not consume Gemini API quota.

## 8. Quick health check

With FastAPI running:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected result:

```text
status
------
ok
```

## 9. Generate a document

Open the Streamlit URL, enter:

1. Document Type
2. Parties Involved
3. Terms & Conditions
4. Effective Date

Click **Generate Document**.

Review and edit the generated draft, then download TXT, DOCX, or PDF.

## 10. Stop the application

In each running terminal press:

```text
Ctrl + C
```

## Troubleshooting

### `uvicorn is not recognized`

Use:

```powershell
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### `streamlit is not recognized`

Use:

```powershell
python -m streamlit run app.py
```

### Gemini API error

Check `.env`, `GEMINI_API_KEY`, the configured `GEMINI_MODEL`, and your Google API quota.

### Frontend cannot connect to backend

Make sure Terminal 1 is running FastAPI on port 8000 and `.env` contains:

```text
BACKEND_URL=http://127.0.0.1:8000
```
