"""Flask UI for the Ops Deadline Tracker. Run: python app.py, then open http://127.0.0.1:5000"""
from datetime import date

from flask import Flask, render_template_string

from tracker import load_tasks, summary

app = Flask(__name__)
TEMPLATE = """
<!doctype html><title>Ops Deadline Tracker</title>
<style>body{font-family:system-ui;margin:2rem} .overdue{color:#b91c1c;font-weight:bold}
.due_today{color:#b45309;font-weight:bold} .due_soon{color:#92400e}
.on_track{color:#166534} .completed{color:#6b7280}</style>
<h1>Ops Deadline Tracker</h1><p>{{ summary }}</p>
<table border=1 cellpadding=8><tr><th>Due</th><th>Client</th><th>Task</th><th>Owner</th><th>Status</th></tr>
{% for t in tasks %}<tr><td>{{ t.due }}</td><td>{{ t.client }}</td><td>{{ t.task }}</td>
<td>{{ t.owner }}</td><td class="{{ t.sla_status(today) }}">{{ t.sla_status(today) }}</td></tr>{% endfor %}
</table>
"""


@app.route("/")
def index():
    today = date.today()
    tasks = sorted(load_tasks("tasks.csv"), key=lambda x: x.due)
    return render_template_string(TEMPLATE, tasks=tasks, today=today, summary=summary(tasks, today))


if __name__ == "__main__":
    app.run(debug=False)
