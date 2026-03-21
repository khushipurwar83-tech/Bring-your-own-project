import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

DATA_FILE = "planner_data.json"

PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}

# -------------------------
# Load / Save
# -------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"tasks": [], "habits": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# TASK SYSTEM
# -------------------------
def add_task(data):
    name = input("Task name: ")
    duration = float(input("Duration (hours): "))
    priority = input("Priority (high/medium/low): ").lower()
    category = input("Category: ")
    deadline = input("Deadline (YYYY-MM-DD optional): ")

    task = {
        "name": name,
        "duration": duration,
        "priority": priority,
        "category": category,
        "deadline": deadline if deadline else None,
        "completed": False,
        "skipped": False
    }

    data["tasks"].append(task)
    save_data(data)
    print("✅ Task added!\n")

def view_tasks(data):
    print("\n--- TASKS ---")
    for i, t in enumerate(data["tasks"], 1):
        status = "Done" if t["completed"] else "Pending"
        print(f"{i}. {t['name']} | {t['priority']} | {t['category']} | {status}")
    print()

def complete_task(data):
    view_tasks(data)
    try:
        i = int(input("Task number: ")) - 1
        data["tasks"][i]["completed"] = True
        save_data(data)
        print("✅ Completed!\n")
    except:
        print("Invalid input\n")

# -------------------------
# HABITS
# -------------------------
def add_habit(data):
    name = input("Habit name: ")
    data["habits"].append({"name": name, "streak": 0})
    save_data(data)
    print("🔥 Habit added!\n")

def complete_habit(data):
    for i, h in enumerate(data["habits"], 1):
        print(f"{i}. {h['name']} (🔥 {h['streak']})")

    try:
        i = int(input("Habit number: ")) - 1
        data["habits"][i]["streak"] += 1
        save_data(data)
        print("✅ Habit updated!\n")
    except:
        print("Invalid\n")

# -------------------------
# SCHEDULER
# -------------------------
def format_time(hour):
    base = datetime.strptime("09:00", "%H:%M")
    return (base + timedelta(hours=hour - 9)).strftime("%I:%M %p")

def auto_reschedule(data):
    for t in data["tasks"]:
        if t["skipped"] and not t["completed"]:
            t["skipped"] = False
            print(f"🔁 Rescheduled: {t['name']}")

def suggestions(data):
    tasks = data["tasks"]

    if any(t["priority"] == "high" and not t["completed"] for t in tasks):
        print("⚠️ You are delaying high priority tasks!")

    if len(tasks) > 8:
        print("⚠️ Too many tasks — risk of burnout!")

    if sum(1 for t in tasks if t["completed"]) < 2:
        print("💡 Start with small tasks to build momentum!")

def generate_schedule(data):
    tasks = data["tasks"]

    if not tasks:
        print("No tasks\n")
        return

    auto_reschedule(data)

    available = float(input("Available hours: "))
    mood = input("Mood (energetic/neutral/tired): ")

    if mood == "energetic":
        tasks = [t for t in tasks if t["priority"] == "high"]
    elif mood == "tired":
        tasks = [t for t in tasks if t["priority"] != "high"]

    tasks = sorted(tasks, key=lambda x: (
        PRIORITY_ORDER[x["priority"]],
        x["deadline"] if x["deadline"] else "9999-12-31"
    ))

    current = 9
    worked = 0

    print("\n--- SMART SCHEDULE ---\n")

    for task in tasks:
        if available <= 0:
            task["skipped"] = True
            continue

        duration = min(task["duration"], available)

        if worked >= 2:
            print(f"{format_time(current)} - {format_time(current+0.5)} → Break ☕")
            current += 0.5
            worked = 0

        print(f"{format_time(current)} - {format_time(current+duration)} → {task['name']}")

        current += duration
        available -= duration
        worked += duration

    print("\n----------------------\n")

    suggestions(data)
    save_data(data)

# -------------------------
# WEEKLY PLAN
# -------------------------
def weekly_plan(data):
    print("\n📅 WEEKLY PLAN\n")
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

    for i, task in enumerate(data["tasks"]):
        print(f"{days[i%7]} → {task['name']}")
    print()

# -------------------------
# ANALYTICS
# -------------------------
def productivity_score(data):
    tasks = data["tasks"]
    if not tasks:
        return

    completed = sum(1 for t in tasks if t["completed"])
    print(f"🔥 Score: {(completed/len(tasks))*100:.2f}%\n")

# -------------------------
# 📊 GRAPHS
# -------------------------
def productivity_graph(data):
    tasks = data["tasks"]
    completed = sum(1 for t in tasks if t["completed"])
    pending = len(tasks) - completed

    plt.figure()
    plt.pie([completed, pending], labels=["Done", "Pending"], autopct="%1.1f%%")
    plt.title("Task Completion")
    plt.show()

def category_graph(data):
    tasks = data["tasks"]
    cat = {}

    for t in tasks:
        cat[t["category"]] = cat.get(t["category"], 0) + 1

    plt.figure()
    plt.bar(cat.keys(), cat.values())
    plt.title("Category Distribution")
    plt.show()

def trend_graph(data):
    tasks = data["tasks"]
    progress = []
    count = 0

    for t in tasks:
        if t["completed"]:
            count += 1
        progress.append(count)

    plt.figure()
    plt.plot(progress)
    plt.title("Productivity Trend")
    plt.show()

# -------------------------
# MAIN MENU
# -------------------------
def main():
    data = load_data()

    while True:
        print("\n==== AI PRO PLANNER ====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Generate Schedule")
        print("5. Weekly Plan")
        print("6. Add Habit")
        print("7. Complete Habit")
        print("8. Productivity Score")
        print("9. Graph: Completion")
        print("10. Graph: Category")
        print("11. Graph: Trend")
        print("12. Exit")

        ch = input("Choice: ")

        if ch == "1": add_task(data)
        elif ch == "2": view_tasks(data)
        elif ch == "3": complete_task(data)
        elif ch == "4": generate_schedule(data)
        elif ch == "5": weekly_plan(data)
        elif ch == "6": add_habit(data)
        elif ch == "7": complete_habit(data)
        elif ch == "8": productivity_score(data)
        elif ch == "9": productivity_graph(data)
        elif ch == "10": category_graph(data)
        elif ch == "11": trend_graph(data)
        elif ch == "12": break
        else: print("Invalid")

if __name__ == "__main__":
    main()
