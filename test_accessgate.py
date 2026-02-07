import unittest
import accessgate


class TestAccessGate(unittest.TestCase):
    def test_unknown_role_counts_as_invalid(self):
        ok, msg = accessgate.check_access("hacker", "view")
        self.assertFalse(ok)
        self.assertIn("Unknown role", msg)

    def test_unknown_action_counts_as_invalid(self):
        ok, msg = accessgate.check_access("guest", "hack_db")
        self.assertFalse(ok)
        self.assertIn("Unknown action", msg)

    def test_guest_cannot_edit(self):
        ok, msg = accessgate.check_access("guest", "edit")
        self.assertFalse(ok)
        self.assertIn("DENY", msg)

    def test_admin_can_delete(self):
        ok, msg = accessgate.check_access("admin", "delete")
        self.assertTrue(ok)
        self.assertIn("ALLOW", msg)

    def test_manager_can_view(self):
        ok, msg = accessgate.check_access("manager", "view")
        self.assertTrue(ok)

    def test_manager_can_edit(self):
        ok, msg = accessgate.check_access("manager", "edit")
        self.assertTrue(ok)

    def test_manager_cannot_delete(self):
        ok, msg = accessgate.check_access("manager", "delete")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
