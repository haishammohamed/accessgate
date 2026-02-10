# AccessGate (RBAC) — Python Mini Project

AccessGate is a small command-line project that demonstrates **Role-Based Access Control (RBAC)**.
It checks whether a user role is allowed to perform an action and returns **ALLOW / DENY** with a reason.

## Features
- RBAC permissions for `admin`, `staff`, and `guest`
- Validates role and action inputs (handles unknown inputs)
- Menu loop (run multiple checks without restarting)
- Simple security behavior: counts invalid inputs and denied attempts and locks out after too many attempts
- Clear messages for each decision

## Roles & Permissions
- **admin**: `view`, `edit`, `delete`, `admin_panel`
- **staff**: `view`, `edit`
- **guest**: `view`

## How it works (logic)
1. User enters username (for display/logging).
2. User chooses “Check access” from the menu.
3. User enters role + action.
4. Program normalizes input (trims spaces, lowercases).
5. Program checks:
   - Is the role known?
   - Is the action known?
   - Is the action allowed for this role?
6. Program prints ALLOW/DENY and updates attempt counters.

## AI-assisted development & testing

This project uses automated tests (`unittest`) to verify behavior.
Changes and new features (e.g. adding a `manager` role) were implemented
with AI assistance and accepted only after all tests passed.

This demonstrates controlled use of AI with verification, not blind code generation.


## Run
```bash
python accessgate.py
