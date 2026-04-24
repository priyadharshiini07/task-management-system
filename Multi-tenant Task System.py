import uuid

# Users
users = [
    {"id": 1, "name": "AdminA", "role": "admin", "org": "A"},
    {"id": 2, "name": "UserA", "role": "member", "org": "A"},
    {"id": 3, "name": "UserB", "role": "member", "org": "B"}
]

# Data storage
tasks = []
logs = []

# CREATE TASK
def create_task(user, title):
    if not title:
        return "Invalid title"

    task = {
        "id": str(uuid.uuid4()),  # unique ID
        "title": title,
        "org": user["org"],
        "created_by": user["id"]
    }

    tasks.append(task)
    logs.append(f"{user['name']} created task '{title}'")
    return task


# VIEW TASKS (Multi-tenant + RBAC)
def view_tasks(user):
    result = []
    for t in tasks:
        if t["org"] == user["org"]:
            if user["role"] == "admin" or t["created_by"] == user["id"]:
                result.append(t)
    return result


# UPDATE TASK
def update_task(user, task_id, new_title):
    if not new_title:
        return "Invalid title"

    for t in tasks:
        if t["id"] == task_id and t["org"] == user["org"]:
            if user["role"] == "admin" or t["created_by"] == user["id"]:
                t["title"] = new_title
                logs.append(f"{user['name']} updated task {task_id}")
                return t
    return "Task not found or Access Denied"


# DELETE TASK
def delete_task(user, task_id):
    for t in tasks:
        if t["id"] == task_id and t["org"] == user["org"]:
            if user["role"] == "admin" or t["created_by"] == user["id"]:
                tasks.remove(t)
                logs.append(f"{user['name']} deleted task {task_id}")
                return "Deleted"
    return "Task not found or Access Denied"


# ------------------ TEST FLOW ------------------

def main():
    current_user = users[1]  # change user here

    print("👤 User:", current_user["name"])

    t1 = create_task(current_user, "Task 1")
    t2 = create_task(current_user, "Task 2")

    print("\n📋 Tasks:", view_tasks(current_user))

    if isinstance(t1, dict):
        update_task(current_user, t1["id"], "Updated Task 1")

    print("\n✏️ After Update:", view_tasks(current_user))

    if isinstance(t2, dict):
        delete_task(current_user, t2["id"])

    print("\n🗑️ After Delete:", view_tasks(current_user))

    print("\n📜 Logs:")
    for log in logs:
        print("-", log)


# Run program
if __name__ == "__main__":
    main()
