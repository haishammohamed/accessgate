# AccessGate v3 - Role Based Access Control (RBAC)

ROLE_PERMISSIONS = {
    "admin": {"view", "edit", "delete", "admin_panel"},
    "staff": {"view", "edit"},
    "guest": {"view"},
    "manager": {"view", "edit"},
}

VALID_ACTIONS = {"view", "edit", "delete", "admin_panel"}

MAX_INVALID_ATTEMPTS = 3
MAX_DENIED_ATTEMPTS = 5

def normalize(text: str) -> str:
    return text.strip().lower()

def check_access(role: str, action: str) -> tuple[bool, str]:
    role = normalize(role)
    action = normalize(action)

    if role not in ROLE_PERMISSIONS:
        return False, f"Unknown role: {role}"
    
    if action not in VALID_ACTIONS:
        return False, f"Unknown action: {action}"

    allowed = action in ROLE_PERMISSIONS[role]
    if allowed:
        return True, f"✅ ALLOW: {role} can {action}"
    return False, f"❌ DENY: {role} cannot {action}"

def main():
    print("=== AccessGate v3 (RBAC) ===")
    username = input("Username: ").strip()
    
    invalid_attempts = 0
    denied_attempts = 0

    while True:
        if invalid_attempts >= MAX_INVALID_ATTEMPTS:
            print("Too many invalid attempts. locked out hu hu 😂😂😂 .")
            break

        if denied_attempts >= MAX_DENIED_ATTEMPTS:
            print("Too many denied access attempts. Access blocked.")
            break

        print("\nChoose an option:")
        print("1. Check Access")
        print("2) Quit")

        choice = input("Enter choice 1 or 2: ").strip()

        if choice == "2":
            print("Goodbye!")
            break

        if choice != "1":
           invalid_attempts += 1
           remaining= MAX_INVALID_ATTEMPTS - invalid_attempts
           print(f"Invalid choice. You have {remaining} attempts left.")
           continue

        role = input("Role (admin/staff/guest): ").strip()
        action = input("Action (view/edit/delete/admin_panel): ").strip()

        ok, message = check_access(role, action)
        print(message)

        if message.startswith("Unknown role") or message.startswith("Unknown action"):
            invalid_attempts += 1
            remaining = MAX_INVALID_ATTEMPTS - invalid_attempts
            print(f"Invalid input. Attempts left: {remaining}")

        # Count denied access (valid inputs but not allowed)
        elif message.startswith("❌ DENY"):
            denied_attempts += 1
            remaining = MAX_DENIED_ATTEMPTS - denied_attempts
            print(f"Denied attempts left before lockout: {remaining}")

        else:
            invalid_attempts = 0  # Reset on valid input
            denied_attempts = 0

            
        # Small extra: show who requested it
        if username:
            print(f"Request by: {username}")

if __name__ == "__main__":
    main()
 

#V3

#NEW FEATURE ADDED
#HERE IN THIS VERSION INVALID ATTEMPTS ADDED TO GET LOCKED OUT AFTER 3 INVALID MENU CHOICE.
#FAILURE : 1  
#HERE THE UNKNOWN ROLE AND UNKNOWN ACTIONS DIDNT SHOW ANY REMAINING ATTEMPTS

#V3.1

#CORRECTED THE FAILED PART IN V3 WHERE UNKNOWN ROLE AND UNKNOWN ACTIONS DIDNT SHOW REMAINING ATTEMPTS
#ADDED 5 FAILED DENIED ATTEMPTS AFTER WHICH ACCESS WILL BE BLOCKED
#FAILURE: 0














