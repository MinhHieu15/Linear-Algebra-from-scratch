"""Daily study reminder for this repo.

    python tools/reminder.py          # always show the window
    python tools/reminder.py --check  # show it only if nothing was committed today
    python tools/reminder.py --week   # also open the week summary
"""

import datetime as dt
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LA = Path(r"D:\Linear Algebra in ML")
PLAYLIST = "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"
STATE = Path.home() / ".la_reminder.json"
TOTAL_DAYS = 60

NEXT_DAY_PROMPT = """\
You are creating Day {n} of a 60-day "Linear Algebra from scratch" study repo (the current directory).
Day {prev} is finished. The learner studies in English; keep the English short and simple.

Read first:
- ROADMAP.md: the row for Day {n} in section 3 (Study, Coding task, Commit) and section "1b. How to study"
  (daily loop, the 3Blue1Brown chapter table, the Core/Bonus rule).
- notebooks/day{prev:02d}_*.ipynb and notes/day{prev:02d}.md: copy their style.
- linalg/ and tests/: the existing library code and test style.

Create:
1. notebooks/day{n:02d}_<short_topic>.ipynb (valid nbformat 4 JSON, kernelspec python3):
   - Title cell "# Day {n:02d} - <topic>": what to watch (the 3Blue1Brown chapter from the table first, if any,
     then the course videos from the Study column), then a short Goal.
   - A first code cell with the imports.
   - "## Core - <name>" section(s): about 45 minutes of work. Then "## Bonus - <name>": optional extras.
   - Each task is a markdown cell starting with "**<ID> - <short name>:**" (IDs like A1, A2, B1), then a one-line
     **Why**, the task, and **Expected:** with the exact output (run the numbers to be sure). Follow it with one
     empty code cell, or a function stub whose body is "...".
   - Last cell: "## Check yourself" with 4-5 questions, answered in a Markdown cell.
   - Easy to harder. Never include solutions.
2. If the Coding task asks for library functions: add them to the right linalg/*.py file as stubs with a docstring
   and `raise NotImplementedError`. Add tests in tests/ that compare against NumPy, each with a line `@DAY{n}` above
   it, where `DAY{n} = pytest.mark.skip(reason="Day {n}: delete the @DAY{n} lines when done")`. The notebook's last
   Core task tells the learner to delete those lines and run pytest.
3. notes/day{n:02d}.md in the style of notes/day{prev:02d}.md: a Watched line, "## Key ideas (in my own words)"
   with 4-6 prompts written as "- <question>:" (nothing after the colon), "## Worked examples by hand" with 2-3 small
   numbered exercises, and "## Still unclear" with "-".

Rules: do not change earlier days' files, README.md or ROADMAP.md. Do not commit. At the end run
`.venv/Scripts/python.exe -m pytest -q`; it must pass (new tests are skipped). Finish with a 3-line summary.
"""

BG, CARD, LINE ="#f6f8fa", "#ffffff", "#d0d7de"
TEXT, MUTED, LINK = "#1f2328", "#656d76", "#0969da"
GREEN, RED, EMPTY = "#2da44e", "#cf222e", "#ebedf0"
FONT = "Segoe UI"
S = 1.0  # display scaling, set in show()


def px(n):
    return int(n * S)


# ---------- data ----------

def run(*cmd, timeout=None):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout,
                          creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def git(*args):
    return run("git", *args).stdout.strip()


def commit_dates():
    return set(git("log", "--since=70.days", "--date=short", "--format=%ad").split())


def streak(dates):
    day = dt.date.today()
    if day.isoformat() not in dates:
        day -= dt.timedelta(days=1)
    n = 0
    while day.isoformat() in dates:
        n += 1
        day -= dt.timedelta(days=1)
    return n


def roadmap():
    """Day -> (study, task, commit message), plus the 3Blue1Brown chapter ranges."""
    rows, chapters = {}, []
    for line in (ROOT / "ROADMAP.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0].isdigit():
            rows[int(cells[0])] = (cells[1], cells[2], cells[3].strip("`"))
        m = re.match(r"\|\s*(\d+)\s*[–-]\s*(\d+)\s*\|\s*(.+?)\s*\|$", line.strip())
        if m:
            chapters.append((int(m[1]), int(m[2]), m[3]))
    return rows, chapters


def current_day():
    days = [int(m[1]) for p in (ROOT / "notebooks").glob("day*.ipynb")
            if (m := re.match(r"day(\d+)", p.name))]
    return max(days, default=1)


def title_of(commit_msg):
    t = commit_msg.split(":", 1)[-1].strip()
    return t[:1].upper() + t[1:]


def empty_cells(day):
    report = notebook_report(day)
    return None if report is None else len(report["empty"])


def notebook_report(day):
    """Task names of empty code cells and of cells that saved an error, plus
    whether the 'Check yourself' questions have an answer cell under them."""
    paths = list((ROOT / "notebooks").glob(f"day{day:02d}_*.ipynb"))
    if not paths:
        return None
    report = {"empty": [], "bonus_left": [], "errors": [], "answered": True}
    task, bonus = "setup", False
    cells = json.loads(paths[0].read_text(encoding="utf-8"))["cells"]
    for i, c in enumerate(cells):
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if c["cell_type"] == "markdown":
            if src.lstrip().startswith("## "):
                bonus = "bonus" in src.splitlines()[0].lower()
            m = re.match(r"\s*\*\*(?:Task )?([^*]+?)\*\*", src)
            if m:
                task = re.split(r" [—-] ", m[1])[0].strip(" :")
            if src.lstrip().startswith("## Check yourself"):
                report["answered"] = any(n["cell_type"] == "markdown" for n in cells[i + 1:])
            continue
        body = [l for l in src.splitlines() if l.strip() and not l.strip().startswith(("def ", "#"))]
        if all(l.strip() == "..." for l in body):
            report["bonus_left" if bonus else "empty"].append(task)  # Bonus never blocks
        if any(o.get("output_type") == "error" for o in c.get("outputs", [])):
            report["errors"].append(task)
    return report


def note_blanks(day):
    blanks = note_blank_list(day)
    return None if blanks is None else len(blanks)


def note_blank_list(day):
    """The prompts in notes/dayXX.md that end with ':' and have no answer."""
    path = ROOT / "notes" / f"day{day:02d}.md"
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    blanks = []
    for i, line in enumerate(lines):
        if not re.match(r"^- .+:\s*$", line):
            continue
        # answered = any text after the prompt, before the next prompt or section
        answer = False
        for nxt in lines[i + 1:]:
            if nxt.startswith(("- ", "## ")):
                break
            if nxt.strip():
                answer = True
                break
        if not answer:
            blanks.append(line[2:].rstrip(" :"))
    return blanks


def child(folder, prefix):
    if folder and folder.exists():
        return next((p for p in sorted(folder.iterdir()) if p.name.startswith(prefix + "_")), None)


def pretty(stem, limit=46):
    words = re.sub(r"^\d+_", "", stem).replace("_assignment", "").replace("-", " ")
    words = words[:1].upper() + words[1:]
    return words if len(words) <= limit else words[:limit - 1] + "…"


def watch_items(day, study, chapters):
    """(icon, label, target) for each thing to watch or open today."""
    items = []
    for lo, hi, text in chapters:
        if lo <= day <= hi:
            for ch in text.split("·"):
                label = re.sub(r"\*", "", ch).replace("(Bonus)", "").strip()
                items.append(("▶", "3B1B " + label, PLAYLIST))
    for part in study.split(";"):
        m = re.search(r"M(\d)\s*›\s*(\d+)(?:\s*›\s*([\d,\s]+))?", part)
        if not m:
            continue
        mod = f"{int(m[1]):02d}"
        section = child(child(child(LA, mod), mod), m[2])
        if not section:
            continue
        for n in re.findall(r"\d+", m[3] or ""):
            f = next(section.glob(f"{int(n):02d}_*.mp4"), None)
            if f:
                items.append(("▶", pretty(f.stem), f))
        if "assignment" in part or not m[3]:
            for f in sorted(section.glob("*_assignment.html")):
                items.append(("✎", pretty(f.stem), f))
    if not any(target != PLAYLIST for _, _, target in items):
        items.append(("•", re.sub(r"[*`]", "", study)[:60], None))
    return items


def load_state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


# ---------- UI ----------

def card(parent, title, right=""):
    outer = tk.Frame(parent, bg=LINE)
    outer.pack(fill="x", padx=14, pady=5)
    inner = tk.Frame(outer, bg=CARD, padx=12, pady=8)
    inner.pack(fill="x", padx=1, pady=1)
    head = tk.Frame(inner, bg=CARD)
    head.pack(fill="x")
    tk.Label(head, text=title, bg=CARD, fg=MUTED, font=(FONT, 9, "bold")).pack(side="left")
    if right:
        tk.Label(head, textvariable=right, bg=CARD, fg=MUTED, font=(FONT, 9)).pack(side="right")
    return inner


def status_row(parent, name, ok, text):
    row = tk.Frame(parent, bg=CARD)
    row.pack(fill="x", pady=1)
    tk.Label(row, text="✓" if ok else "!", width=2, bg=CARD, fg=GREEN if ok else RED,
             font=(FONT, 10, "bold")).pack(side="left")
    tk.Label(row, text=name, width=9, anchor="w", bg=CARD, fg=TEXT, font=(FONT, 10)).pack(side="left")
    tk.Label(row, text=text, bg=CARD, fg=MUTED, font=(FONT, 10)).pack(side="left")


def add_readme_row(day, title):
    """Add 'day | title | links' to the README progress table if it isn't there yet."""
    path = ROOT / "README.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    if any(l.startswith(f"| {day:02d} |") for l in lines):
        return False
    code = [f"[notebook](notebooks/{p.name})" for p in (ROOT / "notebooks").glob(f"day{day:02d}_*.ipynb")]
    for f in git("status", "--short", "--", "linalg").splitlines():
        name = f[3:].strip()
        if name.endswith(".py") and not name.endswith("__init__.py"):
            code.append(f"[{Path(name).name}]({name})")
    row = f"| {day:02d} | {title} | {' · '.join(code)} | [notes](notes/day{day:02d}.md) |"
    start = next(i for i, l in enumerate(lines) if l.startswith("## Progress"))
    last = max(i for i, l in enumerate(lines) if i > start and l.startswith("|"))
    lines.insert(last + 1, row)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def first_commit_date():
    first = git("log", "--reverse", "--date=short", "--format=%ad").split()
    return dt.date.fromisoformat(first[0]) if first else dt.date.today()


def best_streak(dates):
    best = run_ = 0
    prev = None
    for d in sorted(dt.date.fromisoformat(x) for x in dates):
        run_ = run_ + 1 if prev and (d - prev).days == 1 else 1
        best, prev = max(best, run_), d
    return best


def week_window(root, day, dates):
    today = dt.date.today()
    monday = today - dt.timedelta(days=today.weekday())
    week = [monday + dt.timedelta(days=i) for i in range(7)]
    active = sum(d.isoformat() in dates for d in week if d <= today)
    log = git("log", f"--since={monday.isoformat()}T00:00:00", "--date=format:%a", "--format=%ad  %s")

    expected = (today - first_commit_date()).days + 1
    behind = expected - day
    finish = today + dt.timedelta(days=TOTAL_DAYS - day)

    win = tk.Toplevel(root, bg=CARD, padx=px(16), pady=px(12))
    win.title("Week summary")
    win.attributes("-topmost", True)

    def line(text, color=TEXT, bold=False, size=10):
        tk.Label(win, text=text, bg=CARD, fg=color, anchor="w", justify="left",
                 font=(FONT, size, "bold" if bold else "normal")).pack(fill="x")

    line(f"WEEK OF {monday.strftime('%d %b').upper()}", MUTED, True, 9)
    line(f"{active} of {today.weekday() + 1} days active so far", TEXT, True, 16)

    grid = tk.Canvas(win, width=px(7 * 34), height=px(44), bg=CARD, highlightthickness=0)
    grid.pack(anchor="w", pady=(4, 8))
    for i, d in enumerate(week):
        fill = GREEN if d.isoformat() in dates else (EMPTY if d <= today else CARD)
        grid.create_rectangle(px(i * 34), 0, px(i * 34 + 28), px(28), fill=fill, outline=LINE)
        grid.create_text(px(i * 34 + 14), px(38), text="MTWTFSS"[i], fill=MUTED, font=(FONT, 8))

    line("STATS", MUTED, True, 9)
    line(f"   Current streak: {streak(dates)} days   ·   Best: {best_streak(dates)} days")
    line(f"   Day {day} of {TOTAL_DAYS} ({100 * (day - 1) // TOTAL_DAYS}% done)")
    if behind > 0:
        line(f"   {behind} day(s) behind the 1-day-per-day plan. That's fine, steady beats fast.", "#9a6700")
    else:
        line("   On schedule ✓", GREEN)
    line(f"   One day per day from now on: you finish on {finish.strftime('%d %b %Y')}")

    line("\nCOMMITS THIS WEEK", MUTED, True, 9)
    for l in (log.splitlines() or ["   none yet"])[:10]:
        line("   " + l, MUTED)
    tk.Button(win, text="Close", command=win.destroy, padx=10).pack(anchor="e", pady=(10, 0))


def show(week=False):
    global S
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # sharp text on scaled screens
    except (AttributeError, OSError):
        pass
    rows, chapters = roadmap()
    day = current_day()
    study, task, commit_msg = rows.get(day, ("", "", ""))
    dates = commit_dates()
    today = dt.date.today()
    committed = today.isoformat() in dates
    state = load_state()

    root = tk.Tk()
    S = root.winfo_fpixels("1i") / 96
    root.title("Linear Algebra — daily")
    root.configure(bg=BG)
    root.attributes("-topmost", True)
    root.resizable(False, False)

    # header
    head = tk.Frame(root, bg=BG, padx=14, pady=10)
    head.pack(fill="x")
    top = tk.Frame(head, bg=BG)
    top.pack(fill="x")
    tk.Label(top, text=f"DAY {day} / {TOTAL_DAYS}", bg=BG, fg=MUTED, font=(FONT, 9, "bold")).pack(side="left")
    tk.Label(top, text=today.strftime("%a %d %b"), bg=BG, fg=MUTED, font=(FONT, 9)).pack(side="right")
    tk.Label(head, text=title_of(commit_msg), bg=BG, fg=TEXT, font=(FONT, 16, "bold"),
             anchor="w").pack(fill="x")

    bar = tk.Canvas(head, width=px(470), height=px(6), bg=EMPTY, highlightthickness=0)
    bar.pack(anchor="w", pady=(6, 8))
    bar.create_rectangle(0, 0, px(470) * (day - 1) / TOTAL_DAYS, px(6), fill=GREEN, width=0)

    grid_row = tk.Frame(head, bg=BG)
    grid_row.pack(fill="x")
    grid = tk.Canvas(grid_row, width=px(14 * 16), height=px(14), bg=BG, highlightthickness=0)
    grid.pack(side="left")
    for i in range(14):
        d = (today - dt.timedelta(days=13 - i)).isoformat()
        grid.create_rectangle(px(i * 16), 0, px(i * 16 + 12), px(12), width=0,
                              fill=GREEN if d in dates else EMPTY)
    tk.Label(grid_row, text=f"  {streak(dates)}-day streak", bg=BG, fg=TEXT,
             font=(FONT, 10, "bold")).pack(side="left")

    # status pill
    tk.Label(root, text="✓  Committed today" if committed else "●  No commit yet today",
             bg=GREEN if committed else RED, fg="white", font=(FONT, 11, "bold"),
             pady=6).pack(fill="x", padx=14, pady=(0, 5))

    # watch
    items = watch_items(day, study, chapters)
    seen = set(state.get(str(day), []))
    labels = {l for _, l, _ in items}
    count = tk.StringVar(value=f"{len(seen & labels)}/{len(items)}")
    watch = card(root, "WATCH", count)

    def toggle(label, var):
        done = set(state.get(str(day), []))
        done.add(label) if var.get() else done.discard(label)
        state[str(day)] = sorted(done)
        count.set(f"{len(done & labels)}/{len(items)}")
        try:
            STATE.write_text(json.dumps(state), encoding="utf-8")
        except OSError:
            pass

    for icon, label, target in items:
        row = tk.Frame(watch, bg=CARD)
        row.pack(fill="x")
        var = tk.BooleanVar(value=label in seen)
        tk.Checkbutton(row, variable=var, bg=CARD, activebackground=CARD,
                       command=lambda l=label, v=var: toggle(l, v)).pack(side="left")
        lbl = tk.Label(row, text=f"{icon}  {label}", bg=CARD, font=(FONT, 10),
                       fg=LINK if target else TEXT, cursor="hand2" if target else "")
        lbl.pack(side="left")
        if target:
            lbl.bind("<Button-1>", lambda e, t=target: os.startfile(str(t)))

    # do
    do = card(root, "DO")
    cells, blanks = empty_cells(day), note_blanks(day)
    status_row(do, "Notebook", cells == 0,
               "not created" if cells is None else "done" if cells == 0 else f"{cells} cell(s) left")
    status_row(do, "Notes", blanks == 0,
               "not created" if blanks is None else "done" if blanks == 0 else f"{blanks} question(s) left")
    status_row(do, "Commit", committed, commit_msg)

    # uncommitted work
    changed = git("status", "--short").splitlines()
    if changed:
        tk.Label(root, text=f"{len(changed)} file(s) changed but not committed", bg=BG, fg=RED,
                 font=(FONT, 9)).pack(anchor="w", padx=16)

    # next
    if day + 1 in rows:
        nxt = card(root, f"NEXT · DAY {day + 1}")
        nrow = tk.Frame(nxt, bg=CARD)
        nrow.pack(fill="x")
        tk.Label(nrow, text=title_of(rows[day + 1][2]), bg=CARD, fg=TEXT,
                 font=(FONT, 10)).pack(side="left")
        nbr = notebook_report(day)
        day_dirty = git("status", "--short", "--", f"notebooks/day{day:02d}_*", f"notes/day{day:02d}.md")
        ready = (committed and not day_dirty and nbr is not None and not nbr["empty"]
                 and not nbr["errors"] and nbr["answered"] and blanks == 0)
        if ready:
            tk.Button(nrow, text=f"Make Day {day + 1}  ▶", command=lambda: make_next(), bg=GREEN, fg="white",
                      relief="flat", padx=12, pady=2, font=(FONT, 9, "bold")).pack(side="right")
        else:
            tk.Label(nrow, text=f"unlocks when Day {day} is done and committed", bg=CARD, fg=MUTED,
                     font=(FONT, 8)).pack(side="right")

    # buttons
    btns = tk.Frame(root, bg=BG, pady=10)
    btns.pack(fill="x", padx=14)

    def snooze():
        root.withdraw()
        root.after(30 * 60 * 1000, root.deiconify)

    reload = {"again": False}

    def make_next():
        n = day + 1
        claude = shutil.which("claude")
        win = tk.Toplevel(root, bg=CARD, padx=px(16), pady=px(12))
        win.title(f"Make Day {n}")
        win.attributes("-topmost", True)
        win.transient(root)
        win.grab_set()

        def line(text, color=TEXT, bold=False, size=10):
            lbl = tk.Label(win, text=text, bg=CARD, fg=color, anchor="w", justify="left",
                           wraplength=px(420), font=(FONT, size, "bold" if bold else "normal"))
            lbl.pack(fill="x")
            return lbl

        line(f"DAY {n}", MUTED, True, 9)
        line(title_of(rows[n][2]), TEXT, True, 14)
        if not claude:
            line("\nClaude Code (the 'claude' command) was not found, so the app can't write the day. "
                 f"Ask Claude in chat instead: \"Create Day {n}\".", RED)
            tk.Button(win, text="Close", command=win.destroy, padx=10).pack(anchor="e", pady=(10, 0))
            return
        line("\nClaude will create the notebook and the notes for this day, with Core and Bonus tasks, "
             "and add function stubs and tests if the day needs them. It doesn't commit anything.")
        line("Takes about 2–5 minutes and uses your Claude usage.", MUTED)
        status = line("", MUTED)
        row = tk.Frame(win, bg=CARD)
        row.pack(fill="x", pady=(10, 0))
        cancel = tk.Button(row, text="Cancel", command=win.destroy, padx=10)
        cancel.pack(side="right", padx=(6, 0))

        def start():
            go.config(state="disabled")
            cancel.config(state="disabled")
            win.protocol("WM_DELETE_WINDOW", lambda: None)  # don't close while Claude works
            result, t0 = {}, dt.datetime.now()

            def work():
                try:
                    p = subprocess.run(
                        [claude, "-p", "--permission-mode", "acceptEdits", "--allowedTools",
                         "Read,Write,Edit,Glob,Grep,Bash(.venv/Scripts/python.exe -m pytest:*)"],
                        input=NEXT_DAY_PROMPT.format(n=n, prev=day), cwd=ROOT, capture_output=True,
                        encoding="utf-8", errors="replace", timeout=20 * 60,
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                    result["out"] = (p.stdout or p.stderr).strip()
                except subprocess.TimeoutExpired:
                    result["out"] = "Timed out after 20 minutes."

            def poll():
                if "out" not in result:
                    secs = int((dt.datetime.now() - t0).total_seconds())
                    status.config(text=f"Claude is writing Day {n}…  {secs // 60}:{secs % 60:02d}")
                    win.after(1000, poll)
                    return
                made = list((ROOT / "notebooks").glob(f"day{n:02d}_*.ipynb"))
                if made:
                    status.config(text=f"✓ Day {n} is ready: {made[0].name}\n\n{result['out'][-400:]}", fg=GREEN)
                    cancel.config(text=f"Open Day {n}", state="normal", command=lambda: (
                        reload.update(again=True), root.destroy()))
                else:
                    status.config(text="✗ Something went wrong:\n" + result["out"][-400:], fg=RED)
                    cancel.config(text="Close", state="normal", command=win.destroy)
                win.protocol("WM_DELETE_WINDOW", win.destroy)

            threading.Thread(target=work, daemon=True).start()
            poll()

        go = tk.Button(row, text=f"Create Day {n}", command=start, padx=14, bg=GREEN, fg="white")
        go.pack(side="right")

    def check_and_commit():
        root.config(cursor="watch")
        root.update()
        tests = run(sys.executable, "-m", "pytest", "-q")
        root.config(cursor="")
        files = git("status", "--short").splitlines()
        nb = notebook_report(day) or {"empty": ["notebook not created"], "errors": [], "answered": False}
        notes = note_blank_list(day)
        notes = ["notes file not created"] if notes is None else notes

        win = tk.Toplevel(root, bg=CARD, padx=px(16), pady=px(12))
        win.title(f"Day {day} report")
        win.attributes("-topmost", True)
        win.transient(root)
        win.grab_set()

        def line(text, color=TEXT, bold=False, size=10):
            tk.Label(win, text=text, bg=CARD, fg=color, anchor="w", justify="left", wraplength=px(440),
                     font=(FONT, size, "bold" if bold else "normal")).pack(fill="x")

        def check(ok, good, problems):
            if ok:
                line("   ✓  " + good, GREEN)
            for p in problems:
                line("   !  " + p, RED)

        # tests
        line("TESTS", MUTED, True)
        out = tests.stdout.strip().splitlines() or [tests.stderr.strip() or "no output"]
        failed = [l.split(" - ")[0].split("::")[-1] for l in out if l.startswith(("FAILED", "ERROR"))]
        check(tests.returncode == 0, out[-1], [f"{out[-1]}"] + [f"   {t}" for t in failed[:5]]
              if tests.returncode != 0 else [])

        # notebook
        line("\nNOTEBOOK", MUTED, True)
        problems = ([f"Empty: {', '.join(nb['empty'])}"] if nb["empty"] else []) + \
                   ([f"Saved an error: {', '.join(nb['errors'])} (fix it, then Run All)"] if nb["errors"] else []) + \
                   ([] if nb["answered"] else ["'Check yourself' not answered (add a Markdown cell)"])
        check(not problems, "Every task done", problems)

        # notes
        short = [q.replace("`", "") for q in notes]
        short = [q if len(q) <= 45 else q[:44] + "…" for q in short]
        line(f"\nNOTES  (notes/day{day:02d}.md)" + (f": {len(notes)} unanswered" if notes else ""), MUTED, True)
        check(not notes, "Every question answered",
              short[:6] + ([f"… {len(notes) - 6} more"] if len(notes) > 6 else []))

        # files
        line(f"\nFILES TO COMMIT ({len(files)})", MUTED, True)
        for f in files[:8]:
            line("   " + f, MUTED)
        if len(files) > 8:
            line(f"   … and {len(files) - 8} more", MUTED)

        # verdict
        finished = not problems and not notes
        if tests.returncode != 0:
            verdict, color, can_commit = "✗  Tests are failing. Fix them before committing.", RED, False
        elif not files:
            verdict, color, can_commit = "Nothing to commit. Save your files first (Ctrl+K S).", MUTED, False
        elif finished:
            verdict, color, can_commit = f"✓  Day {day} is complete. Ready to commit!", GREEN, True
            if not any(l.startswith(f"| {day:02d} |") for l in (ROOT / "README.md").read_text(encoding="utf-8").splitlines()):
                verdict += f"\n    (Day {day} will be added to the README progress table.)"
        else:
            verdict, color, can_commit = "◐  Tests pass, but the day isn't finished. You can commit it as WIP.", "#9a6700", True
        line("")
        line(verdict, color, True, 11)
        default = commit_msg if finished else f"wip: day {day:02d} {title_of(commit_msg).lower()}"

        if not can_commit:
            tk.Button(win, text="Close", command=win.destroy, padx=10).pack(anchor="e", pady=(10, 0))
            return

        line("\nCOMMIT MESSAGE", MUTED, True)
        msg = tk.Entry(win, width=48, font=(FONT, 10))
        msg.insert(0, default)
        msg.pack(fill="x", pady=4)
        result = tk.Label(win, text="", bg=CARD, font=(FONT, 10, "bold"), anchor="w", justify="left")
        result.pack(fill="x")
        row = tk.Frame(win, bg=CARD)
        row.pack(fill="x", pady=(8, 0))

        def done():
            reload["again"] = True
            root.destroy()

        def do_commit():
            go.config(state="disabled")
            if finished:
                add_readme_row(day, title_of(commit_msg))
            run("git", "add", "-A")
            c = run("git", "commit", "-m", msg.get().strip() or default)
            if c.returncode != 0:
                result.config(text="Commit failed:\n" + (c.stderr or c.stdout).strip()[:300], fg=RED)
                go.config(state="normal")
                return
            result.config(text="✓ Committed. Pushing to GitHub…", fg=GREEN)
            pushed = {}

            def push():
                try:
                    pushed["ok"] = run("git", "push", timeout=60).returncode == 0
                except subprocess.TimeoutExpired:
                    pushed["ok"] = False

            def wait():
                if "ok" not in pushed:
                    win.after(300, wait)
                    return
                result.config(text="✓ Committed and pushed. Your square is green!" if pushed["ok"] else
                              "✓ Committed (it counts for today).\n! Push failed. Run 'git push' later.",
                              fg=GREEN if pushed["ok"] else RED)
                cancel.config(text="Done", command=done)

            threading.Thread(target=push, daemon=True).start()
            wait()

        cancel = tk.Button(row, text="Cancel", command=win.destroy, padx=10)
        cancel.pack(side="right", padx=(6, 0))
        go = tk.Button(row, text="Commit", command=do_commit, padx=14, bg=GREEN, fg="white")
        go.pack(side="right")

    for text, cmd in [("Close", root.destroy), ("Snooze", snooze),
                      ("Week", lambda: week_window(root, day, dates)),
                      ("Open VS Code", lambda: subprocess.Popen(f'code "{ROOT}"', shell=True)),
                      ("✓ Check", check_and_commit)]:
        tk.Button(btns, text=text, command=cmd, relief="flat", bg=CARD, fg=TEXT, padx=10, pady=3,
                  font=(FONT, 9), highlightbackground=LINE).pack(side="right", padx=(6, 0))

    root.update_idletasks()
    w, h = px(500), root.winfo_reqheight()
    root.geometry(f"{w}x{h}+{root.winfo_screenwidth() - w - px(24)}+{px(40)}")
    root.bell()
    if week or (today.weekday() == 6 and state.get("week_shown") != today.isoformat()):
        state["week_shown"] = today.isoformat()  # auto-show once every Sunday
        try:
            STATE.write_text(json.dumps(state), encoding="utf-8")
        except OSError:
            pass
        root.after(300, lambda: week_window(root, day, dates))
    root.mainloop()
    return reload["again"]


if __name__ == "__main__":
    if "--check" in sys.argv and dt.date.today().isoformat() in commit_dates():
        sys.exit(0)
    lock = socket.socket()
    try:
        lock.bind(("127.0.0.1", 47613))  # only one window at a time
    except OSError:
        sys.exit(0)
    week = "--week" in sys.argv
    while show(week):  # reopen with fresh status after a commit
        week = False
