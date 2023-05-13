import unittest

from app import db, create_app, client
from app.user.models import User
from config import DebugConfiguration


class TestClientController(unittest.TestCase):
    current_user = None

    def setUp(self) -> None:
        self.app = create_app(DebugConfiguration)
        self.app.app_context().push()

        db.create_all()

        current_user = User("test_user", "a-very-secure-password")
        db.session.add(current_user)
        db.session.commit()

        self.current_user = User.query.filter_by(username="test_user").first()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app.app_context()

    # Testing CRUD operations

    def test_create_client(self):
        created_client = client.controllers.create(self.current_user, "My awesome client")

        self.assertIsNotNone(created_client)

        self.assertEqual(created_client.owner, self.current_user)
        self.assertEqual(created_client._name, "My awesome client")

        self.assertIsNotNone(created_client.id)

        self.assertIs(created_client.is_confidential, True)
        self.assertIs(created_client.is_pubic, False)

    def test_update_client(self):
        pass

    def test_read_client(self):
        pass

    def test_read_all_clients(self):
        pass

    def test_delete_client(self):
        pass

    # Testing CRUD edge cases

    def test_create_duplicate_client(self):
        pass

    def test_update_protected_client_property(self):
        pass

    def test_delete_non_existent_client(self):
        pass


if __name__ == '__main__':
    unittest.main()
