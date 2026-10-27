"""Ops Deadline Tracker — core logic.

Reads tasks from a CSV with columns: id, client, task, owner, due_date (YYYY-MM-DD), status
(status is 'open' or 'done'). Classifies each open task by deadline and
generates a short follow-up draft for anything that needs chasing.

Run:  python tracker.py tasks.csv
"""
import csv
import sys
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Task:
    id: str
    client: str
    task: str
    owner: str
    due: date
    done: bool

    def sla_status(self, today: date) -> str:
        if self.done:
            return "completed"
        if self.due < today:
            return "overdue"
        if self.due == today:
            return "due_today"
        if self.due <= today + timedelta(days=3):
            return "due_soon"
        return "on_track"

    def follow_up_draft(self, today: date) -> str:
        status = self.sla_status(today)
        if status == "overdue":
            days = (today - self.due).days
            return (f"Hi {self.client} team — following up on '{self.task}'. "
                    f"It was due {self.due} ({days} day(s) ago). "
                    f"Could you share an updated ETA today?")
        if status == "due_today":
            return (f"Hi {self.client} team — quick check on '{self.task}', "
                    f"due today ({self.due}). Is it on track to close today?")
        if status == "due_soon":
            return (f"Hi {self.client} team — '{self.task}' is due {self.due}. "
                    f"Just confirming there is nothing blocking it.")
        return ""


def load_tasks(path: str) -> list[Task]:
    tasks = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            y, m, d = (int(x) for x in row["due_date"].split("-"))
            tasks.append(Task(
                id=row["id"], client=row["client"], task=row["task"],
                owner=row["owner"], due=date(y, m, d),
                done=row["status"].strip().lower() == "done",
            ))
    return tasks


def summary(tasks: list[Task], today: date) -> dict:
    counts = {"overdue": 0, "due_today": 0, "due_soon": 0,
              "on_track": 0, "completed": 0}
    for t in tasks:
        counts[t.sla_status(today)] += 1
    return counts


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "tasks.csv"
    today = date.today()
    tasks = load_tasks(path)
    print(f"Tasks: {len(tasks)}  |  Today: {today}")
    print("Summary:", summary(tasks, today))
    print()
    for t in sorted(tasks, key=lambda x: x.due):
        print(f"[{t.sla_status(today):>10}] {t.due}  {t.client} — {t.task} (owner: {t.owner})")
        draft = t.follow_up_draft(today)
        if draft:
            print(f"             Draft: {draft}")


if __name__ == "__main__":
    main()
