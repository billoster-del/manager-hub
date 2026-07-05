# Manager Hub

A local automation system that imports Dayforce schedule exports, processes them,
and publishes the results for online viewing.

## Quick Start

```bash
./setup.sh
source venv/bin/activate
uvicorn app.main:app --reload
```

## Project Structure

```
scripts/      — Automation pipeline (import, convert, clean, map, export, archive)
app/          — FastAPI web application
config/       — Shift mappings, staff data, SMTP settings
imports/      — Drop Dayforce .xls exports here
archive/      — Processed originals
output/       — Generated XLSX, PDF, reports
```

## Stack

- **Python 3.13** — automation engine
- **FastAPI + Jinja2** — web viewer
- **LibreOffice** — XLS→XLSX + PDF export
- **Tesseract** — OCR
- **Cloudflare Pages** — deployment
- **GitHub Actions** — CI
