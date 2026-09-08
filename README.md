# CreatorOS

CreatorOS is an approval-gated AI operating system for a local-business lead-generation service. The first operating configuration is **gyms in Hyderabad** with trial-class enquiries as the primary KPI.

## Product workflow

1. Research local gyms and prepare a lightweight social audit.
2. Run the COO intelligence pipeline: Trend Hunter → Niche Researcher → deterministic Niche Ranking → Opportunity Generator → COO Evaluation → Safety Gate.
3. Generate local-language content and personalized outreach drafts.
4. Review claims and approve customer-facing sends or a mission.
5. Approved missions are planned and executed as internal AI tasks; generated artifacts remain approval-gated.
6. Record replies, qualified leads, appointments, and trial-class enquiries.
7. Report operating signals and escalate warnings or errors.

AI handles routine research, drafting, classification, scoring, planning, and reporting. The owner remains in control of payments, contracts, refunds, financial commitments, account recovery, legal/medical/financial claims, customer-data deletion, publishing, outreach sends, and other external actions.

## Architecture

- **Backend:** FastAPI + SQLAlchemy + SQLite by default.
- **AI:** Gemini through the existing AI Brain integration. Structured-output parsing and validation protect downstream services from malformed model responses.
- **Employees:** CEO-facing COO/Business Partner, Trend Hunter, Niche Researcher, Niche Ranking, Opportunity Generator, Mission Planner, Mission Executor, Content Employee, and Product Employee.
- **Approval system:** drafts, outreach, mission approvals, and generated artifacts carry explicit approval state and action class. CreatorOS does not silently publish or send external communications.
- **Mission execution:** Mission Planner creates dependency-aware tasks. Mission Executor runs only after owner approval, validates outputs, persists artifacts, and records failures. External delivery remains a separate approval step.
- **Long-running jobs:** Morning Brief and approved Mission execution run in an in-process background job manager so the HTTP request returns immediately. Job status is exposed through polling endpoints and the Mission Control UI. This local MVP job state is intentionally non-durable and should be replaced by a persistent queue when deployed beyond a single process.
- **Frontend:** Next.js + React + TypeScript + Tailwind + Framer Motion, with the existing premium dark CEO dashboard and dedicated Mission Control view.

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
python -m uvicorn app.main:app --reload --port 8000
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

## Key API flows

### Morning Brief

- `POST /morning-brief` or `POST /morning-brief/refresh` starts the COO pipeline without blocking the request.
- `GET /morning-brief` returns the latest high-level state.
- `GET /morning-brief/{job_id}` returns job progress, result, or failure details.

### Mission approval and execution

- `POST /approve-mission` records the CEO decision and starts an approved mission in the background.
- `GET /missions/{job_id}` exposes mission progress, tasks, artifacts, approval state, and errors.
- Mission execution never sends or publishes externally; generated customer-facing artifacts remain reviewable in the approval center.

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

## Current limitations

- The local job manager is process-local and loses in-flight job state after a backend restart.
- External Instagram publishing and message sending are intentionally not connected; CreatorOS prepares and gates those actions instead.
- Live market/trend values must not be interpreted as verified platform analytics unless a live data integration is explicitly connected.
- Production deployment should add durable job storage, authentication/authorization, observability, rate limits, and a production database.

## Future upgrades

1. Durable background jobs and persistent mission/job history.
2. Authenticated multi-business workspaces and role-based approvals.
3. Verified social-platform analytics and publishing integrations.
4. Richer prospect enrichment and CRM integrations.
5. Production observability, audit logs, and deployment automation.
