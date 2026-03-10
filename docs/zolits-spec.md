## ZOLITS – Issue Tracking System Specification

This document translates the existing Google Sheet **“Operations Workstream Post go-live issues”** into a real‑time multi‑user web application called **ZOLITS**.

The focus is to:
- Preserve all current data and workflows
- Automate repetitive work (IDs, timestamps, capitalization, reminders)
- Provide dashboards and Slack notifications
- Support clean roles and permissions (Admin, Regional Manager, Expert)

---

### 1. Core Concepts and Roles

- **Region**: Logical area such as `SOUTHERN`, `WESTERN`, `EASTERN`, `HARARE`, `HEAD OFFICE`, etc. (from the workbook tabs and `DEPOT` column values).
- **Depot**: More specific location within a region (e.g., `GWERU`, `KWEKWE`, `ZVISHAVANE`).
- **Issue**: Single row from the current sheet; becomes one record in the main `issues` table.
- **User**:
  - **Admin**
    - Creates all user accounts (Regional Managers, Experts, other Admins if needed)
    - Manages reference data (regions, depots, modules, severity/status lists)
    - Has full CRUD across the system
  - **Regional Manager**
    - Logs new issues for their region(s)
    - Assigns an issue to a specific **Expert**
    - Sets severity and status via dropdowns
    - Can update descriptive fields until marked Resolved
    - Can change their password
  - **Expert**
    - Sees all issues (not only assigned ones)
    - Can pick up and resolve any issue
    - When they change status to a resolved state, they are automatically recorded as **Issue Resolved By**
    - Receives Slack notifications when:
      - Newly assigned
      - Assigned critical issues are still open (repeated reminders)

Authentication:
- Email/username + password (hashed)
- Admin creates accounts; users can change their own passwords via “Change Password” screen.

---

### 2. Data Model

#### 2.1. Tables Overview

- **users**
- **roles**
- **regions**
- **depots**
- **modules**
- **issue_severity**
- **issue_status**
- **issues**
- **issue_history** (audit log)
- **attachments**
- **settings** (e.g., reminder frequency)

#### 2.2. Users and Roles

**roles**
- `id` (PK)
- `name` (`ADMIN`, `REGIONAL_MANAGER`, `EXPERT`)

**users**
- `id` (PK)
- `full_name`
- `email` (unique, used for login)
- `password_hash`
- `role_id` (FK → roles.id)
- `region_id` (nullable FK → regions.id; required for Regional Managers)
- `is_active` (boolean)
- `created_at`
- `updated_at`

> Admin UI: create user, select role, select region (for Regional Managers), optionally link to Slack user ID (for notifications).

#### 2.3. Regions and Depots

**regions**
- `id` (PK)
- `name` (e.g., `SOUTHERN`, `WESTERN`, `EASTERN`, `NORTHERN`, `HARARE`, `HEAD OFFICE`)
- `code` (short string if needed)

**depots**
- `id` (PK)
- `region_id` (FK → regions.id)
- `name` (e.g., `GWERU`, `KWEKWE`, `ZVISHAVANE`)

#### 2.4. Reference Data – Modules, Severity, Status

**modules**
- `id` (PK)
- `name` (e.g., `CRM`, `SMART VEND`, `CONTRACTING`, `TARIFF CHANGE`, `ALL`, `ZUMS`)

**issue_severity**
- `id` (PK)
- `name` (e.g., `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
- `priority_order` (integer, lower = more important)

**issue_status**
- `id` (PK)
- `name` (e.g., `PENDING`, `ISSUE RECEIVED`, `WORK IN PROGRESS`, `NEEDS CLARIFICATION`, `RESOLVED`)
- `is_resolved_state` (boolean)

> The exact list is seeded based on the current sheet values (normalised spelling).

#### 2.5. Issues Table – Main Single Source of Truth

**issues**
- `id` (PK, internal numeric)
- `issue_number` (string, e.g., `SU32`, `SU101`)
  - Auto‑generated following existing pattern:
    - Prefix derived from region: `SU` = SOUTHERN; extendable for other regions (`WE`, `EA`, etc.) – confirm and configure in settings.
    - Numeric part = incrementing sequence **per region/prefix**.
- `region_id` (FK → regions.id) – from dropdown
- `depot_id` (FK → depots.id)
- `module_id` (FK → modules.id)
- `functionality` (string, uppercase)
- `description` (text, uppercase) – corresponds to `ISSUE DESCRIPTION`
- `raised_by_name` (string, uppercase) – `ISSUE RAISED BY`
- `contact_phone` (string)
- `issue_logged_by_id` (FK → users.id) – Regional Manager user
- `assigned_to_id` (FK → users.id, role = EXPERT)
- `severity_id` (FK → issue_severity.id)
- `status_id` (FK → issue_status.id)
- `date_issue_raised` (datetime) – automatically set on submit (even if UI shows separate date/time)
- `time_issue_raised` (time) – optional separate field if you want to preserve the sheet layout; otherwise derived from `date_issue_raised`
- `resolution_notes` (text, uppercase) – maps to `RESOLUTION`
- `zetdc_comments` (text)
- `longshine_comments` (text)
- `code` (string) – from sheet
- `release_date` (date / datetime)
- `tracker` (string)
- `issue_resolved_by_id` (FK → users.id)
- `date_issue_resolved` (datetime)
- `created_at`
- `updated_at`

**Uppercasing rule**
- On backend save:
  - Convert these fields to uppercase:
    - `functionality`
    - `description`
    - `raised_by_name`
    - `resolution_notes`
    - Any free‑text “title” fields intended to be uppercase as per sheet style
  - Phone numbers, codes, and comments that must preserve formatting should **not** be forced to uppercase.

#### 2.6. Attachments

**attachments**
- `id` (PK)
- `issue_id` (FK → issues.id)
- `file_name`
- `file_path` or `storage_url`
- `uploaded_by_id` (FK → users.id)
- `uploaded_at`

Supported uploads:
- At minimum: image formats (`.png`, `.jpg`, `.jpeg`, `.gif`) as “screenshot”.
- Later extend to PDFs or other formats if needed.

#### 2.7. Audit History

**issue_history**
- `id` (PK)
- `issue_id` (FK → issues.id)
- `changed_by_id` (FK → users.id)
- `changed_at` (datetime)
- `field_name` (string)
- `old_value` (text)
- `new_value` (text)

Used for:
- Tracking who changed status, severity, assignee, comments, etc.
- Supporting reporting such as “how long issues spent in CRITICAL state”.

---

### 3. Workflows and UI Behavior

#### 3.1. Login and Roles

- **Login Page**
  - Email + password
  - On success:
    - Admin → Admin Dashboard
    - Regional Manager → Regional Manager Dashboard (for their region)
    - Expert → Expert Dashboard (issues assigned to them + all issues list)

#### 3.2. Regional Manager – Log New Issue

**New Issue Form (Regional Manager view)**
- Fields:
  - Region: dropdown (pre‑filled with the manager’s region; can be locked or left changeable depending on policy)
  - Depot: dropdown filtered by selected Region
  - Module: dropdown (CRM, SMART VEND, etc.)
  - Functionality: text input (auto‑uppercased on save)
  - Issue Description: multi‑line text (auto‑uppercased on save)
  - Issue Raised By: text input (auto‑uppercased)
  - Contact Phone Number: text
  - Screenshot: file upload (optional, 1+ files)
  - Issue Assigned To: dropdown of Experts (user.role = EXPERT)
  - Issue Severity: dropdown from `issue_severity` (CRITICAL, HIGH, MEDIUM, etc.)
  - Issue Status: dropdown from `issue_status` (default = `ISSUE RECEIVED` or `PENDING` – configurable)

**Automations on Submit**
- **Issue ID**:
  - System determines prefix from Region (e.g., SOUTHERN → `SU`).
  - Fetches the last issue with same prefix, increments numeric part:
    - e.g., last = `SU103` → new = `SU104`.
  - Saves as `issue_number`.
- **Timestamps**:
  - `date_issue_raised` = current datetime.
  - Optionally also populate separate `date` and `time` fields if UI requires.
- **Uppercasing**:
  - Backend enforces uppercase for configured text fields regardless of how user types.
- **Slack Notification**:
  - On initial creation:
    - Send a Slack DM (or channel message) to the assigned Expert:
      - Template:  
        > “HEY {EXPERT_NAME}, YOU HAVE A NEW {SEVERITY_NAME} ISSUE ({ISSUE_NUMBER}) WITH STATUS {STATUS_NAME}.”
    - Include basic details and a link to the issue in ZOLITS.

#### 3.3. Issue List and Row Coloring

Issue table views (for all roles) follow color rules:

- **Base colors by Status**:
  - `RESOLVED` → row highlighted **faint green**
  - `PENDING` or equivalent waiting state → row highlighted **faint gray**
- **Critical behavior overriding**:
  - If `severity = CRITICAL` and issue is **not in a resolved state** (`is_resolved_state = false`):
    - Row highlighted **red**.
  - If `severity = CRITICAL` **and** status is a resolved state:
    - Row highlighted **faint green** (resolved overrides).
  - For non‑critical issues:
    - Colors follow status only (green for resolved, gray for pending, neutral/other colors for intermediate states).

The logic can be represented as:
- If `status.is_resolved_state = true` → green
- Else if `severity = CRITICAL` → red
- Else if `status.name = 'PENDING'` → faint gray
- Else → default / neutral styling.

#### 3.4. Expert – Managing and Resolving Issues

**Expert view**
- My Issues:
  - List issues assigned to the logged‑in Expert.
  - Summaries: counts by severity/status, charts.
- All Issues:
  - Full table (filtered/searchable).
  - Experts are allowed to:
    - Change status (e.g., from `WORK IN PROGRESS` to `RESOLVED`)
    - Add/update resolution notes
    - Reassign to themselves or others if process allows

**Automatic “Issue Resolved By” and Resolution Timestamp**
- When an Expert changes status from a non‑resolved state to a resolved state:
  - System sets:
    - `issue_resolved_by_id` = current user ID
    - `date_issue_resolved` = current datetime
  - Also logs a row in `issue_history`.

**Resolving Issues Not Initially Assigned**
- If an Expert who is not `assigned_to_id` updates status to a resolved state:
  - The system **still** records them as `issue_resolved_by_id`.
  - Optionally, `assigned_to_id` may be left as original assignee (to keep assignment history) or auto‑updated to the resolver – policy decision; default is to leave `assigned_to_id` unchanged and only track resolver in `issue_resolved_by_id`.

#### 3.5. Editing Existing Issues

- **Regional Managers**:
  - Can edit description, functionality, `raised_by_name`, `contact_phone`, `assigned_to`, `severity`, and `status` **until** issue is resolved.
  - After resolution, Regional Managers can add comments but cannot change core attributes (to protect audit trail), unless Admin grants permissions.
- **Experts**:
  - Can change status, severity, resolution notes, and optionally reassign issues.
- **Admin**:
  - Can edit anything, including correcting data migration mistakes.

All changes are logged in `issue_history`.

---

### 4. Notifications and Reminders

#### 4.1. Slack Integration

Configuration:
- Store a global Slack Bot token and per‑user Slack identifiers (user ID or mapped email) in system settings.

Events:
- **On new issue creation**:
  - Notify assigned Expert with a message including:
    - Issue number, severity, status, region, depot, module, and short description.
- **On reassignment**:
  - Notify new Expert.
- **On status change to Resolved**:
  - Optionally notify the Regional Manager that opened the issue.

#### 4.2. Critical Issue Reminders

Background job (e.g., hourly task via scheduler/cron/Windows Task Scheduler) executes:

- Query:
  - All issues where:
    - `severity = CRITICAL`
    - `status.is_resolved_state = false`
- For each such issue:
  - Send Slack reminder to `assigned_to_id` (if any):
    - Template:  
      > “REMINDER: YOU HAVE AN OPEN CRITICAL ISSUE ({ISSUE_NUMBER}) – CURRENT STATUS: {STATUS_NAME}.”
  - Optionally send a summary to Regional Manager for that region.

Configuration in `settings`:
- Reminder frequency (default: every hour).
- Whether to send reminders only during working hours.

---

### 5. Dashboards and Reporting

The system should provide **daily, weekly, and monthly** summary views and exportable reports.

#### 5.1. Global Admin Dashboard

Widgets:
- **Issue Volume by Region**
  - Bar chart: Region vs. count of issues (filterable by date range).
- **Status Breakdown**
  - Pie/donut chart: Resolved, Pending, Work in Progress, Needs Clarification, etc.
- **Severity Breakdown**
  - Counts of Critical, High, Medium, Low (with trend over time).
- **SLA‑like metrics (if defined)**
  - Average time to resolution overall and per region/module.

Filters:
- Date range (today, last 7 days, last 30 days, custom)
- Region
- Module
- Severity

#### 5.2. Regional Dashboard (Regional Manager)

For the manager’s region:
- **Total issues** in selected period
- **Resolved vs Unresolved**
- **By severity** (Critical/High/etc.)
- **By status**
- **Top problem modules** (CRM, SMART VEND, ZUMS, etc.)
- **Issue list** for that region with color‑coded rows.

Exports:
- CSV / Excel export for regional reports.

#### 5.3. Expert Performance Dashboard

Per Expert:
- Number of issues **assigned** to them (current and historical)
- Number of issues **resolved by** them
- Breakdown by severity:
  - How many critical issues they resolved
- Average time to resolve per severity

Visuals:
- Bar chart: Experts vs. number of issues resolved
- Leaderboard table: top resolvers in a given period.

---

### 6. Data Migration from Existing Sheet

Goal: single `issues` table with all regions’ data.

Steps:
- Export Google Sheet tab(s) to CSV.
- For each row:
  - Map columns:
    - `ISSUE NUMBER` → `issue_number`
    - `DEPOT` → map to `depots.name` (also sets `region_id` from the tab name or DEPOT column if consistent)
    - `MODULE` → `modules.name`
    - `FUNCTIONALITY` → `functionality`
    - `ISSUE DESCRIPTION` → `description`
    - `ISSUE RAISED BY` → `raised_by_name`
    - `CONTACT PHONE NUMBER` → `contact_phone`
    - `SCREENSHOT` URL / info → create `attachments` records if possible, or store URL in comments.
    - `ISSUE LOGGED BY` → map to a Regional Manager `user` if matchable.
    - `ISSUE ASSIGNED TO` → map to Expert `user`.
    - `DATE ISSUE RAISED` and `TIME` → `date_issue_raised` (normalize formats like `19/01/24`, `21.01.26`, etc.).
    - `ISSUE SEVERITY` → `severity_id` (normalize cases like `HIGH`, `High`).
    - `ISSUE STATUS` → `status_id`.
    - `RESOLUTION` → `resolution_notes`.
    - `DATE RESOLVED` → `date_issue_resolved`.
    - `ZETDC COMMENTS`, `LONGSHINE COMMENTS`, `CODE`, `RELEASE DATE`, `TRACKER` → respective fields.
  - Uppercase the designated text fields on import to match new system’s style.

Validation:
- Any rows with missing or invalid data are logged for manual review.

---

### 7. Technology‑Agnostic Implementation Outline

You can implement ZOLITS with any web stack (e.g., Node/Express + React, Django, Laravel, ASP.NET, etc.). Regardless of stack, the key components are:

- **Backend API**
  - Authentication endpoints (login, change password)
  - Issues CRUD endpoints (with role‑based access control)
  - File upload endpoint for screenshots
  - Slack integration endpoint/service
  - Scheduled job for critical reminders
- **Frontend**
  - Login + password change screens
  - Separate dashboards for Admin, Regional Managers, Experts
  - Issue creation/edit forms with dropdowns, file upload, and validation
  - Data tables with filtering, search, and conditional row colors
  - Charts for dashboards
- **Database**
  - Implement schema described in section 2.
  - Indexes on:
    - `issue_number`
    - `region_id`, `severity_id`, `status_id`
    - `assigned_to_id`, `issue_resolved_by_id`
    - `date_issue_raised`, `date_issue_resolved`

---

### 8. Security and Access Control

- All endpoints require authentication except login.
- Role‑based authorization:
  - **Admin**: full access.
  - **Regional Manager**: can only create/edit issues for their region; read‑only access to other regions (or none, depending on policy).
  - **Expert**: can view all issues; can change status/resolution and add comments; cannot change system settings or user accounts.
- Input validation:
  - Sanitize all text input to avoid injection attacks.
  - Validate file types and sizes for uploads.
- Passwords stored using a modern hashing algorithm (e.g., bcrypt/argon2).

---

### 9. Next Implementation Steps

If you want, the next step is:
- Choose a specific tech stack (e.g., React + FastAPI + PostgreSQL).
- I will then:
  - Generate database migration scripts for the schema above.
  - Scaffold backend endpoints and models.
  - Scaffold a modern, user‑friendly UI (dashboards, forms, tables) that reflects all behaviors described here, including uppercase enforcement, auto‑IDs, timestamps, colors, and Slack notifications.

