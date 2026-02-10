import csv
import uuid
from datetime import datetime

CATEGORIES = {"access", "network", "system_failure", "phishing"}
STATUSES = {"OPEN", "IN_PROGRESS", "CLOSED"}
CSV_FIELDS = ["ticket_id", "created_at", "user", "category", "blocked", "priority", "status", "description"]

def normalize(text: str) -> str:
    return text.strip().lower()

def yes_no(prompt: str) -> bool:
    while True:
        answer = normalize(input(prompt))
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please type yes/no (y/n).")

def calculate_priority(category: str, blocked: bool) -> str:
    category = normalize(category)

    if category == "phishing":
        return "HIGH"
    if category == "network":
        return "HIGH" if blocked else "MEDIUM"
    if category == "access":
        return "MEDIUM" if blocked else "LOW"
    if category == "system_failure":
        return "MEDIUM" if blocked else "LOW"

    return "LOW"

def create_ticket(user: str, category: str, blocked: bool, description: str) -> dict:
    ticket_id = str(uuid.uuid4())[:8]
    created_at = datetime.now().isoformat(timespec="seconds")
    priority = calculate_priority(category, blocked)

    return {
        "ticket_id": ticket_id,
        "created_at": created_at,
        "user": user.strip(),
        "category": normalize(category),
        "blocked": str(blocked),
        "priority": priority,
        "status": "OPEN",
        "description": description.strip()
    }

def load_tickets(filename: str = "tickets.csv") -> list[dict]:
    try:
        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []

def save_all_tickets(tickets: list[dict], filename: str = "tickets.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(tickets)

def append_ticket(ticket: dict, filename: str = "tickets.csv"):
    tickets_exist = False
    try:
        with open(filename, "r", encoding="utf-8"):
            tickets_exist = True
    except FileNotFoundError:
        tickets_exist = False

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not tickets_exist:
            writer.writeheader()
        writer.writerow(ticket)

def list_tickets(tickets: list[dict], title: str):
    print(f"\n=== {title} ===")
    if not tickets:
        print("No tickets to display.")
        return

    for t in tickets:
        print(
            f"ID: {t['ticket_id']} | "
            f"User: {t['user']} | "
            f"Category: {t['category']} | "
            f"Blocked: {t['blocked']} | "
            f"Priority: {t['priority']} | "
            f"Status: {t['status']} | "
            f"Created: {t['created_at']}"
        )
        print(f"  Description: {t['description']}")

def filter_menu(tickets: list[dict]):
    if not tickets:
        print("No tickets found.")
        return

    while True:
        print("\nView tickets:")
        print("1) All tickets")
        print("2) OPEN tickets")
        print("3) HIGH priority tickets")
        print("4) MEDIUM priority tickets")
        print("5) IN_PROGRESS tickets")
        print("6) CLOSED tickets")
        print("7) Back")

        choice = input("Choose 1-7: ").strip()

        if choice == "7":
            return

        if choice == "1":
            list_tickets(tickets, "All Tickets")
        elif choice == "2":
            list_tickets([t for t in tickets if t["status"] == "OPEN"], "OPEN Tickets")
        elif choice == "3":
            list_tickets([t for t in tickets if t["priority"] == "HIGH"], "HIGH Priority Tickets")
        elif choice == "4":
            list_tickets([t for t in tickets if t["priority"] == "MEDIUM"], "MEDIUM Priority Tickets")
        elif choice == "5":
            list_tickets([t for t in tickets if t["status"] == "IN_PROGRESS"], "IN_PROGRESS Tickets")
        elif choice == "6":
            list_tickets([t for t in tickets if t["status"] == "CLOSED"], "CLOSED Tickets")
        else:
            print("Invalid choice.")


def update_status(tickets: list[dict]) -> bool:
    if not tickets:
        print("No tickets to update.")
        return False

    ticket_id = input("Enter ticket ID to update: ").strip()
    found = None
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            found = t
            break

    if not found:
        print("Ticket not found.")
        return False

    print(f"Current status: {found['status']}")
    new_status = input("New status (OPEN / IN_PROGRESS / CLOSED): ").strip().upper()

    if new_status not in STATUSES:
        print("Invalid status.")
        return False

    found["status"] = new_status
    print("Status updated ✅")
    return True

def filter_open(tickets: list[dict]) -> list[dict]:
    return [t for t in tickets if t["status"] == "OPEN"]

def filter_high(tickets: list[dict]) -> list[dict]:
    return [t for t in tickets if t["priority"] == "HIGH"]

def main():
    print("=== Helpdesk v3 ===")

    while True:
        print("\nChoose an option:")
        print("1) Create ticket")
        print("2) View tickets")
        print("3) Update ticket status")
        print("4) Quit")

        choice = input("Enter 1-4: ").strip()

        if choice == "1":
            user = input("Who are you? (name or role): ").strip()

            category = normalize(input("Category (access/network/system_failure/phishing): "))
            if category not in CATEGORIES:
                print(f"Invalid category. Choose one of: {', '.join(sorted(CATEGORIES))}")
                continue

            blocked = yes_no("Are you blocked from working? (y/n): ")
            description = input("Describe the problem in one line: ").strip()

            ticket = create_ticket(user, category, blocked, description)
            append_ticket(ticket)

            print("\nTicket created ✅")
            print(f"ID: {ticket['ticket_id']}")
            print(f"Priority: {ticket['priority']}")
            print(f"Status: {ticket['status']}")
            continue
        if choice == "2":
            tickets = load_tickets()
            filter_menu(tickets)
            continue

        if choice == "3":
            tickets = load_tickets()
            changed = update_status(tickets)
            if changed:
                save_all_tickets(tickets)
            continue

        if choice == "4":
            print("Goodbye!")
            break

        print("Invalid choice.")

if __name__ == "__main__":
    main()
