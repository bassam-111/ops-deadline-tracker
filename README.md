# Ops Deadline Tracker

A small operations tool for people who juggle many client tasks at once:
it reads tasks from a CSV, flags what is overdue / due today / due soon,
and drafts a polite follow-up message for anything that needs chasing.

This is the kind of tool an Operations Executive actually uses every day:
less time checking spreadsheets, fewer missed deadlines, faster follow-ups.

## Run the CLI

```bash
python tracker.py tasks.csv
```

## Run the web UI

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Task file format

`tasks.csv` columns: `id, client, task, owner, due_date (YYYY-MM-DD), status (open/done)`

## Status rules

- `overdue` — due date is before today
- `due_today` — due today
- `due_soon` — due within the next 3 days
- `on_track` — due later
- `completed` — status is `done`

## Built with

Python (standard library for the core logic) + Flask for the UI. No database
needed — swap `tasks.csv` for your own task list and it just works.
