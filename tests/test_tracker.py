from datetime import date
from pathlib import Path

from tracker import load_tasks, summary


def test_summary_classifies_sample_tasks():
    tasks = load_tasks(Path(__file__).parents[1] / "tasks.csv")

    assert summary(tasks, date(2026, 10, 28)) == {
        "overdue": 2,
        "due_today": 0,
        "due_soon": 1,
        "on_track": 1,
        "completed": 1,
    }


def test_sample_task_statuses_and_follow_up():
    tasks = load_tasks(Path(__file__).parents[1] / "tasks.csv")
    today = date(2026, 10, 28)

    assert tasks[0].sla_status(today) == "overdue"
    assert "1 day(s) ago" in tasks[0].follow_up_draft(today)
    assert tasks[2].sla_status(today) == "due_soon"
    assert tasks[3].sla_status(today) == "on_track"
    assert tasks[4].sla_status(today) == "completed"
    assert tasks[4].follow_up_draft(today) == ""
