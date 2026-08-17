# CreatorOS

CreatorOS is an approval-gated AI operating system for a local-business lead-generation service. The first operating configuration is **gyms in Hyderabad** with trial-class enquiries as the primary KPI.

## Product workflow

1. Research local gyms and prepare a lightweight social audit.
2. Generate local-language content and personalized outreach drafts.
3. Review claims and approve customer-facing sends.
4. Record replies, qualified leads, appointments, and trial-class enquiries.
5. Report the operating signals and escalate warnings or errors.

AI handles routine research, drafting, classification, and reporting. The owner remains in control of payments, contracts, refunds, financial commitments, account recovery, legal/medical/financial claims, customer-data deletion, and external sends.

## Workspace boundary

All project work belongs in this directory:

`C:\Users\LOQ\OneDrive\Desktop\CreatorOS`

The unrelated `Downloads\CreatorOS\CreatorOS` directory must not be accessed or changed.

## Backend setup

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

The backend uses SQLite at `creatoros.db` by default. Set `CREATOROS_DATABASE_URL` for another SQLAlchemy-supported database and `CREATOROS_FRONTEND_ORIGINS` for comma-separated allowed browser origins.

Gemini generation requires `GEMINI_API_KEY`. `GEMINI_MODEL` is optional and defaults to the model configured in `app/services/ai_brain.py`. Health and operational read endpoints remain available when the key is missing; generation reports a configuration error.

## Frontend setup

```bash
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

Set `NEXT_PUBLIC_API_URL` when the API is not at `http://127.0.0.1:8000`.

## Verification

```bash
cd backend
python -m compileall -q app
pytest -q

cd ../frontend
npm run lint
npx tsc --noEmit
npm run build
```

AI-provider, TTS, avatar, and video calls should be mocked in automated tests. Generated media, SQLite files, virtual environments, secrets, and caches are ignored by the root `.gitignore`.
