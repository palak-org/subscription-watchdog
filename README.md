# Subscription Watchdog - Input & Security Layer (Phase 1) 🚀

## Overview

This repository provides the **frontend UI** and **data parsing layer** for an AI‑powered subscription‑tracking tool. It offers a modern, secure Web 2.0 interface where users can upload their billing statements (CSV or PDF). The uploaded files are parsed into a clean JSON array, ready for downstream ingestion by an LLM **Extraction Agent**.

---

## Features ✨

- **Secure Web 2.0 UI** – polished card layout, gradient background, flexbox, and responsive design.
- **File validation** – only `.csv` or `.pdf` files under **5 MB** are accepted, with client‑side checks.
- **Mock session authentication** – `sessionStorage`‑based `authToken` flow with login/logout buttons for easy local testing.
- **BOM / hidden‑character sanitisation** – removes invisible Unicode markers and surrounding quotes from CSV headers and cells.
- **Asynchronous statement parser** – `parseStatement(file)` reads the file, parses CSV rows, or (via **pdf.js**) extracts PDF text, applies regex extraction and returns a **stringified JSON** array of transactions.

---

## Strict Data Requirements **(CRITICAL)** 📋

### Accepted File Formats
- **CSV** – must contain the **exact** header row:
  ```
  Date,Description,Amount,Type
  ```
  The parser is case‑insensitive but expects these column names (after sanitisation).

- **PDF** – each transaction line must follow the pattern:
  ```
  MM/DD/YYYY - Description - $Amount
  ```
  The internal regex `/\d{2}\/\d{2}\/\d{4}\s*-\s*(.*?)\s*-\s*\$([\d.]+)/g` relies on this exact format.

> **Note**: The `mock_data` folder (included in the repo) contains example CSV and PDF files that conform to the required specifications.

---

## How to Run 🖥️

1. **Clone the repo** (if you haven't already) and navigate to the project root:
   ```bash
   cd path/to/your/cloned-repo
   ```
2. **Start a simple local server** (Python is the easiest):
   ```bash
   python -m http.server 8000
   ```
3. Open a browser and go to:
   ```bash
   http://localhost:8000/src/ui/upload_form.html
   ```
   The UI will load, allowing you to log in (mock) and upload statements.

---

## Architecture Note 🏗️

The repository’s sole responsibility is to **output a clean JSON array of transaction objects** (`[{date, description, amount}]`). This JSON is intended for direct consumption by an **LLM Extraction Agent** downstream in the Subscription Watchdog pipeline. No additional processing, storage, or backend services are included in Phase 1.

---

## License

This project is provided under the **MIT License** – feel free to use, modify, and distribute.
