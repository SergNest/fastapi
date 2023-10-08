from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schema import ContactModel


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def upcoming_birthdays(db: Session):
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        (Contact.date_of_birth >= today) & (Contact.date_of_birth <= end_date)
    ).all()
    return contacts


async def read_contacts(db: Session, name, surname, email):
    contacts = db.query(Contact)
    if name:
        contacts = contacts.filter(Contact.name.ilike(f"%{name}%"))
    if surname:
        contacts = contacts.filter(Contact.surname.ilike(f"%{surname}%"))
    if email:
        contacts = contacts.filter(Contact.email.ilike(f"%{email}%"))
    return contacts.all()


async def get_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def update_contact(body: ContactModel, contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.name = body.name,
        contact.surname = body.surname,
        contact.phone_number = body.phone_number,
        contact.date_of_birth = body.date_of_birth,
        contact.description = body.description,
        contact.email = body.email
        db.commit()
    return contact


async def remove_contact(owner_id: int, db: Session):
    owner = db.query(Contact).filter_by(id=owner_id).first()
    if owner:
        db.delete(owner)
        db.commit()
    return owner
