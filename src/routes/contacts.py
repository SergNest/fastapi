from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.schema import ResponseContact, ContactModel
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.post("/", response_model=ResponseContact, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.get("/", response_model=List[ResponseContact])
async def get_contacts(db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contacts(db)
    return contact


@router.get("/upcoming_birthdays", response_model=List[ResponseContact])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    contact = await repository_contacts.upcoming_birthdays(db)
    return contact


@router.get("/find", response_model=List[ResponseContact])
async def read_contacts(db: Session = Depends(get_db), name: str = Query(None, alias="name"),
                                 surname: str = Query(None, alias="surname"),
                                 email: str = Query(None, alias="email")):
    contact = await repository_contacts.read_contacts(db, name, surname, email)
    return contact


@router.get("/{contact_id}", response_model=ResponseContact)
async def get_contact(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(owner_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return contact


@router.put("/{contact_id}", response_model=ResponseContact)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return contact

