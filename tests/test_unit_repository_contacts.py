import unittest
from datetime import datetime, timedelta, date
from unittest.mock import MagicMock


from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schema import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    upcoming_birthdays,
    read_contacts,
    update_contact
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(len(result), len(contacts))
        for contact in result:
            self.assertIsInstance(contact, Contact)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(user=self.user, contact_id=1, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(user=self.user, contact_id=1,  db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(name="Serg", surname="Testovich", email="s.nester@gmail.com", phone_number='+380732044873',
                            date_of_birth=date(1986, 1, 12), description="test contact")
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.date_of_birth, body.date_of_birth)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(user=self.user, contact_id=1, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_upcoming_birthdays(self):

        today = datetime.now().date()
        self.session.query().filter().all.return_value = [
            Contact(date_of_birth=today + timedelta(days=i), user=self.user) for i in range(1, 8)
        ]

        result = await upcoming_birthdays(user=self.user, db=self.session)

        for contact in result:
            self.assertTrue(today <= contact.date_of_birth <= today + timedelta(days=7))

    async def test_read_contacts(self):
        self.session.query().filter().all.return_value = [
            Contact(name="John", surname="Doe", email="john@example.com", user=self.user),
            Contact(name="Jane", surname="Doe", email="jane@example.com", user=self.user),
        ]

        result = await read_contacts(user=self.user, db=self.session, name="John", surname="", email="")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "John")

    async def test_update_contact(self):
        existing_contact = Contact(
            id=1, name="OldName", surname="OldSurname", phone_number="123456789",
            date_of_birth=datetime(1990, 1, 1), description="Old description",
            email="old@example.com", user=self.user
        )
        self.session.query().filter().first.return_value = existing_contact

        updated_contact_model = ContactModel(
            name="NewName", surname="NewSurname", phone_number="987654321",
            date_of_birth=date(1995, 5, 5),  # Use date from datetime module
            description="New description",
            email="new@example.com"
        )

        result = await update_contact(
            body=updated_contact_model, contact_id=1, user=self.user, db=self.session
        )

        self.assertEqual(result.name, ("NewName",))
        self.assertEqual(result.surname, ("NewSurname",))
        self.assertEqual(result.phone_number, ("987654321",))
        self.assertEqual(result.date_of_birth, (date(1995, 5, 5),))
        self.assertEqual(result.description, ("New description",))
        self.assertEqual(result.email, "new@example.com")


if __name__ == '__main__':
    unittest.main()
