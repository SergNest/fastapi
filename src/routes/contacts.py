from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.database.models import User
from src.schema import ResponseContact, ContactModel
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.post("/", response_model=ResponseContact, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input, which is validated by pydantic.
        The current_user is retrieved from the auth_service and passed to repository_contacts for validation purposes.
        A database session is also passed to repository_contacts.

    :param body: ContactModel: Pass the contact model to the function
    :param current_user: User: Get the user that is currently logged in
    :param db: Session: Get the database session
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


@router.get("/", response_model=List[ResponseContact], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contacts(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts for the current user.
        The function takes in two parameters:
            - current_user: A User object that represents the currently logged-in user. This is passed in by FastAPI's Depends() method, which calls auth_service.get_current_user().
            - db: A Session object that represents an open database connection to our PostgreSQL database, passed in by FastAPI's Depends() method, which calls get_db().

    :param current_user: User: Get the current user, and db: session is used to connect to the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contacts(current_user, db)
    return contact


@router.get("/upcoming_birthdays", response_model=List[ResponseContact], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_upcoming_birthdays(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The get_upcoming_birthdays function returns a list of contacts with upcoming birthdays.
        The current_user parameter is the user who is currently logged in and making the request.
        The db parameter is an instance of Session that will be used to query the database.

    :param current_user: User: Get the current user
    :param db: Session: Pass the database session to the function
    :return: A list of contacts that have upcoming birthdays
    :doc-author: Trelent
    """
    contact = await repository_contacts.upcoming_birthdays(current_user, db)
    return contact


@router.get("/find", response_model=List[ResponseContact], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def read_contacts(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db),
                        name: str = Query(None, alias="name", ),
                        surname: str = Query(None, alias="surname"),
                        email: str = Query(None, alias="email")):
    """
    The read_contacts function is used to read all contacts from the database.
        The function takes in a current_user, db, name, surname and email as parameters.
        It then calls the read_contacts function from repository_contacts which returns a contact object.

    :param current_user: User: Get the user that is currently logged in
    :param db: Session: Get the database session
    :param name: str: Search for a contact by name
    :param alias: Make the query parameter name different from the function argument
    :param ): Specify the number of items to be returned
    :param surname: str: Filter the contacts by surname
    :param alias: Change the name of the parameter in the query string
    :param email: str: Query the database for a specific email address
    :param alias: Change the name of the parameter in the query string
    :return: A list of contacts that match the search criteria
    :doc-author: Trelent
    """
    contact = await repository_contacts.read_contacts(current_user, db, name, surname, email)
    return contact


@router.get("/{contact_id}", response_model=ResponseContact, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contact(current_user: User = Depends(auth_service.get_current_user), contact_id: int = Path(ge=1),
                      db: Session = Depends(get_db)):
    """
    The get_contact function returns a contact by its ID.

    :param current_user: User: Get the current user from the auth_service
    :param contact_id: int: Specify the id of the contact to be retrieved
    :param db: Session: Inject the database session into the function
    :return: A contact object, which is defined in the models
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return contact


@router.put("/{contact_id}", response_model=ResponseContact)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1),
                         current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id of the contact to be updated, and a body containing all fields that are to be updated.
        If no fields are provided, then nothing is changed in the database.

    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Specify the id of the contact to be deleted
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Get the database session
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The delete_contact function deletes a contact from the database.
        The function takes in an integer representing the id of the contact to be deleted,
        and returns a dictionary containing information about that contact.

    :param contact_id: int: Specify the contact id to be deleted
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Get the database session
    :return: The deleted contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return contact
