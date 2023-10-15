from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schema import ContactModel


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(**body.dict(), user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(user: User, db: Session) -> Contact | None:
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def upcoming_birthdays(user: User, db: Session):
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        (Contact.date_of_birth >= today) & (Contact.date_of_birth <= end_date) & (Contact.user_id == user.id)
    ).all()
    return contacts


async def read_contacts(user: User, db: Session, name, surname, email):
    contacts = db.query(Contact)
    if name:
        contacts = contacts.filter(Contact.name.ilike(f"%{name}%") & (Contact.user_id == user.id))
    if surname:
        contacts = contacts.filter(Contact.surname.ilike(f"%{surname}%") & (Contact.user_id == user.id))
    if email:
        contacts = contacts.filter(Contact.email.ilike(f"%{email}%") & (Contact.user_id == user.id))
    return contacts.all()


async def get_contact(user: User, contact_id: int, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def update_contact(body: ContactModel, contact_id: int, user: User, db: Session):
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
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
