from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schema import ContactModel


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Pass the contact data to be created
    :param user: User: Get the user_id from the token
    :param db: Session: Access the database
    :return: The created contact
    :doc-author: Trelent
    """
    contact = Contact(**body.dict(), user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(user: User, db: Session) -> Contact | None:
    """
    The get_contacts function returns a list of contacts for the user with the given id.


    :param user: User: Get the user's id
    :param db: Session: Pass the database session to the function
    :return: A list of contact objects, not a single object
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def upcoming_birthdays(user: User, db: Session):
    """
    The upcoming_birthdays function returns a list of contacts whose birthdays are within the next 7 days.

    :param user: User: Identify the user who is requesting the upcoming birthdays
    :param db: Session: Pass in the database session to the function
    :return: A list of contacts that have birthdays in the next 7 days, including today
    :doc-author: Trelent
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        (Contact.date_of_birth >= today) & (Contact.date_of_birth <= end_date) & (Contact.user_id == user.id)
    ).all()
    return contacts


async def read_contacts(user: User, db: Session, name, surname, email):
    """
    The read_contacts function returns a list of contacts that match the given name, surname and email.
        If no parameters are provided, all contacts will be returned.

    :param user: User: Get the user's id from the database
    :param db: Session: Pass the database session to the function
    :param name: Filter the contacts by name
    :param surname: Filter the contacts by surname
    :param email: Filter the contacts by email
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact)
    if name:
        contacts = contacts.filter(Contact.name.ilike(f"%{name}%") & (Contact.user_id == user.id))
    if surname:
        contacts = contacts.filter(Contact.surname.ilike(f"%{surname}%") & (Contact.user_id == user.id))
    if email:
        contacts = contacts.filter(Contact.email.ilike(f"%{email}%") & (Contact.user_id == user.id))
    return contacts.all()


async def get_contact(user: User, contact_id: int, db: Session):
    """
    The get_contact function returns a contact object from the database.
        Args:
            user (User): The user who is requesting the contact.
            contact_id (int): The id of the requested Contact object.
            db (Session): A connection to our database, used for querying and updating data.

    :param user: User: Get the user from the database
    :param contact_id: int: Filter the contact by id
    :param db: Session: Pass the database session to the function
    :return: The contact with the given id if it exists, otherwise none
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session):
    """
    The update_contact function updates a contact in the database.
        Args:
            body (ContactModel): The updated contact information.
            contact_id (int): The id of the contact to update.
            user (User): The user who is updating the contact. This is used for authorization purposes, as only a logged-in
                user can update their own contacts and not those of other users.

    :param body: ContactModel: Get the contact data from the request body
    :param contact_id: int: Identify the contact to be updated
    :param user: User: Get the user id from the token
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name,
        contact.surname = body.surname,
        contact.phone_number = body.phone_number,
        contact.date_of_birth = body.date_of_birth,
        contact.description = body.description,
        contact.email = body.email
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact. This is used to ensure that only contacts belonging to this
                user are deleted, and not contacts belonging to other users with similar IDs.

    :param contact_id: int: Specify the id of the contact to be deleted
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: The contact object if it exists, otherwise none
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

