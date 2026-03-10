## ZOLITS local hosting (Windows)

### Backend (Django)

From `backend/`:

```powershell
python manage.py migrate

# seed reference data (roles, region/depots, modules, severities, statuses)
python manage.py seed_zolits

# optional: create sample expert/regional manager accounts
python manage.py seed_zolits --with-sample-users

python manage.py runserver 0.0.0.0:8000
```

Media uploads (screenshots) will be served at:
- `http://localhost:8000/media/...` (DEBUG mode only)

### Frontend (React)

From `frontend/`:

```powershell
npm install
npm run dev
```

Open:
- `http://localhost:5173`

### Slack notifications

Set environment variable:
- `SLACK_BOT_TOKEN` = your Slack bot token (e.g. `xoxb-...`)

For each Expert user, set their Slack DM target:
- In Django admin → **ZOLITS CORE → User profiles**
- Set `slack_user_id` to the user’s Slack ID (example: `U012ABCDEF`)

### Critical reminders (hourly)

Run manually:

```powershell
python manage.py send_critical_reminders
```

#### Windows Task Scheduler setup

- Open **Task Scheduler**
- Create Task…
  - **Name**: `ZOLITS Critical Reminders`
  - **Trigger**: Daily → Repeat task every **1 hour** → for duration of **1 day**
  - **Action**: Start a program
    - Program/script: `C:\Users\ze9172535\AppData\Local\Programs\Python\Python314\python.exe` (adjust if different)
    - Add arguments:
      - `manage.py send_critical_reminders`
    - Start in:
      - `c:\Users\ze9172535\Documents\snyamudo\ZO LITS\backend`

