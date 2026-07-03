# 🐕 Subscription Watchdog

> Your personal AI watchdog for subscription overspending — detect, alert, track and cancel, automatically.

**Hackathon:** AI Agents: Intensive Vibe Coding Capstone Project  
**Track:** Concierge Agents  
**Submitted:** July 3, 2026

---

## 📌 What is this?

Subscription Watchdog is a multi-agent Python application that solves a problem almost everyone quietly struggles with — losing track of recurring subscriptions. Streaming services, software tools, and cloud plans renew silently every month, prices change without warning, and small charges pile up unnoticed.

It takes your bank statement (CSV or PDF), automatically identifies every recurring subscription, compares it against previous scans stored in a local SQLite database, and raises clear actionable alerts when something changes — new subscription detected, price increased, or service going unused. For unused subscriptions, it generates a ready-to-send cancellation email on the spot.

---

## 🚨 Problem Statement

Recurring subscriptions are "invisible spending." A subscription never requires an active decision to keep paying — it just renews. People underestimate subscription spending, miss price increases, and keep paying for services they no longer use.

Manual review means reading every statement line, mentally tagging subscriptions, remembering previous charges, and deciding what to keep. Tedious, easy to skip, error-prone. Subscription Watchdog replaces all of that with an automated, repeatable check.

---

## 🎯 Project Goals

1. **Automatic subscription detection** — extract name, currency, and amount from raw statement text or uploaded CSV/PDF
2. **Change detection over time** — SQLite memory stores previous scans; alerts on what's new or changed
3. **Usage-based alerts** — flag subscriptions unused for extended periods
4. **Actionable output** — don't just inform; generate a cancellation email on the spot

---

## 🏗️ System Architecture

```

Bank Statement (CSV / PDF)
         │
         ▼
┌─────────────────────────────────────────────┐
│  PHASE 1 — Input & Security                 │
│  Bhalala Palak (@palak-org)                 │
│                                             │
│  ├── Secure Web 2.0 UI (HTML/JS/CSS)        │
│  ├── File validation (CSV/PDF, max 5MB)     │
│  ├── Mock session auth (sessionStorage)     │
│  ├── BOM & hidden-character sanitisation    │
│  ├── Auth & Login Check    [SECURITY REQ]   │
│  ├── Input Sanitization    [SECURITY REQ]   │
│  └── statement_parser.py                   │
│       CSV → DictReader rows                 │
│       PDF → pdf.js regex extraction         │
│       Output: clean JSON [{date,desc,amt}]  │
└──────────────────┬──────────────────────────┘
                   │ Clean JSON
                   ▼
┌─────────────────────────────────────────────┐
│  PHASE 2 — AI Extraction Agent              │
│  Akshay Sharma (@Akshay-23A)                │
│                                             │
│  ├── Gemini Multi-Agent System  [ADK REQ]   │
│  ├── extractorm1.py                         │
│  │    Classifier Agent                      │
│  │    → Merchant detect                     │
│  │      (Netflix, Spotify, Amazon Prime…)   │
│  │    Extractor Agent                       │
│  │    → Price & billing cycle               │
│  └── Output: Structured subscription        │
│  |     objects → passed to Phase 3           |
|  |------- final Readme                      |
└──────────────────┬──────────────────────────┘
                   │ Subscription list
                   ▼
┌─────────────────────────────────────────────┐
│  PHASE 3 — Memory + MCP Server              │
│  Raju Palanki (@Timothy-Raju)               │
│                                             │
│  ├── memorym2.py                            │
│  │    load_memory()  → fetch history        │
│  │    save_memory()  → persist scan         │
│  ├── database/db.py                         │
│  │    SQLite — subscriptions table          │
│  │    (id, name, amount, currency,          │
│  │     created_at)                          │
│  └── MCP Server    [MCP SERVER REQ]         │
│       get_subs / add_sub / flag_sub         │
└──────────────────┬──────────────────────────┘
                   │ History + current scan
                   ▼
┌─────────────────────────────────────────────┐
│  PHASE 4 + 5 — Decision Engine + CLI +      │
│  Integration & Submission                   │
│  Manoj A Sankena (@manojnasankena)          │
│                                             │
│  ├── decisionm3.py                          │
│  │    Price & usage logic                   │
│  │    Flags: unused / overpriced /          │
│  │           trial-ending                   │
│  │    Alert rules: price spike /            │
│  │                 duplicate / trial end    │
│  ├── orchestrator.py                        │
│  │    SubscriptionPipeline.run()            │
│  │    Category mapping (streaming/saas/…)   │
│  ├── main.py — run_watchdog()               │
│  │    Wires all 4 modules together          │
│  │    Integration tests, end-to-end         │
│  ├── CLI entry point  [AGENT CLI REQ]       │
│  ├── ui/app.py — Streamlit Web UI           │
│  ├── Email drafts + Watchdog Report         │
│  │    → passes final data to Lead           │
│  └── Final report + submit Jul 6   │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
      ✅ Subscription Watchdog — Live & Submitted
      All 6 submission requirements demonstrated

```

---

## 📁 Project Structure

```
subscription-watchdog/
├── agents/
│   ├── extractorm1.py       # Phase 2 — Gemini extraction agent
│   ├── memorym2.py          # Phase 3 — Memory agent (SQLite load/save)
│   ├── decisionm3.py        # Phase 4 — Decision engine & alert logic
│   ├── orchestrator.py      # Phase 4 — SubscriptionPipeline coordinator
│   ├── statement_parser.py  # Phase 1 — CSV parser (DictReader)
│   └── iphandler.py         # Phase 1 — CLI input handler
├── database/
│   ├── __init__.py
│   └── db.py                # SQLite — get_connection(), init_db()
├── data/
│   ├── sample_statement.csv # Sample CSV (Date, Description, Amount, Type)
│   └── sample_statement.pdf # Sample PDF
├── mock_data/               # Example CSV & PDF files (spec-compliant)
├── src/
│   └── ui/
│       └── upload_form.html # Phase 1 — Secure Web 2.0 upload UI
├── ui/
│   ├── __init__.py
│   ├── app.py               # Phase 4 — Streamlit web frontend
│   └── input_handler.py     # Phase 4 — get_user_input() for CLI
├── main.py                  # Orchestrator — run_watchdog(), run_project()
├── requirements.txt         # google-generativeai, python-dotenv
├── .gitignore               # __pycache__, *.pyc, .env, *.db
└── .env                     # GEMINI_API_KEY, DATABASE_URL (not committed)

```

---

## ⚙️ The Watchdog Pipeline

`run_watchdog()` in `main.py` runs a clean sequential pipeline:

| Step | Function | Action |
|------|----------|--------|
| 1 | `get_user_input()` | Collect raw statement text from user |
| 1.5 | `parse_statement()` | Parse CSV/PDF → structured JSON rows |
| 2 | `extract_subscriptions()` | Identify subscriptions — name, currency, amount |
| 3 | `load_memory()` | Load previous scan history from SQLite |
| 4 | `run_decision_engine()` | Compare current vs history → generate alerts |
| 5 | Print Watchdog Report | Show alerts with type-specific formatting |
| 5b | `save_memory()` | Persist current scan for next run's comparison |

---

## 🚨 Alert Types

| Alert | Trigger | Output |
|-------|---------|--------|
| 🆕 `new` | Subscription not in previous scans | Name + amount displayed |
| 📈 `price_increase` | Same subscription, higher amount than memory | Old → New amount shown side by side |
| ⚠️ `possible_cancel` | Subscription unused for extended period | Type YES → cancellation email generated instantly |

---

## 🖥️ Installation & Running

### Option A — Web UI (Streamlit)
```bash
# 1. Clone the repo
git clone https://github.com/manojnasankena/subscription-watchdog
cd subscription-watchdog

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment — create a .env file:
GEMINI_API_KEY=your_key_here

# 4. Run
streamlit run ui/app.py
```

### Option B — Phase 1 Upload UI (HTML)
```bash
# Navigate to project root and start local server
python -m http.server 8000

# Open in browser:
# http://localhost:8000/src/ui/upload_form.html
```

### Option C — CLI
```bash
python main.py
```

> **Note:** SQLite database (`database/subscriptions.db`) is auto-created on first run via `init_db()`. No setup needed.

---

## 📋 Accepted File Formats

**CSV** — must contain this exact header row:
```
Date,Description,Amount,Type
```

**PDF** — each transaction line must follow:
```
MM/DD/YYYY - Description - $Amount
```

Sample files that conform to these specs are in the `mock_data/` folder.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3, JavaScript, HTML/CSS |
| AI / Extraction | Google Gemini API (`google-generativeai`) |
| Agent Orchestration | Gemini ADK — Multi-agent pipeline |
| Web UI | Streamlit + Secure HTML/JS upload form |
| PDF Parsing | pdf.js (Phase 1 UI) |
| Database | SQLite (`sqlite3`) |
| CSV Parsing | Python `csv.DictReader` |
| Env Config | `python-dotenv` |

---

## 👥 Team

| Phase | Responsibility | Contributor | GitHub |
|-------|---------------|-------------|--------|
| Phase 1 | Input & Security — Secure Web UI, File Validation, Auth, CSV/PDF Parser | Bhalala Palak | [@palak-org](https://github.com/palak-org) |
| Phase 2 | AI Extraction — Gemini ADK, Merchant Detection, Price & Cycle | Akshay Sharma | [@Akshay-23A](https://github.com/Akshay-23A) |
| Phase 3 | Memory + MCP Server — SQLite persistence, get/save/flag subs | Raju Palanki | [@Timothy-Raju](https://github.com/Timothy-Raju) |
| Phase 4+5 | Decision Engine + CLI + Integration + Submission | Manoj A Sankena | [@manojnasankena](https://github.com/manojnasankena) |

---

## 🔮 Future Directions

- Support more statement formats — UPI exports, budgeting app CSVs, more bank PDF layouts
- Wider merchant recognition beyond Netflix / Spotify / Amazon Prime
- Duplicate subscription detection across family accounts
- Trial-to-paid conversion date alerts
- PostgreSQL backend for multi-user support
- Month-over-month spending trend reports

---
---

## License

This project is provided under the **MIT License** – feel free to use, modify, and distribute.
---
---
