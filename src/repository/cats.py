from sqlalchemy.orm import Session

from src.database.models import Cat
from src.schema import PetModel, PetStatusVaccinated


async def create_cat(body: PetModel, db: Session):
    cat = Cat(**body.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


async def get_cats(limit: int, offset: int, owner_id: int, is_vaccinated: bool, db: Session):
    cats = db.query(Cat)
    if owner_id:
        cats = cats.filter(Cat.owner_id == owner_id)
    if is_vaccinated is not None:
        cats = cats.filter(Cat.vaccinated == is_vaccinated)
    cats = cats.limit(limit).offset(offset).all()
    return cats


async def get_cat(cat_id: int, db: Session):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    return cat


async def update_cat(body: PetModel, cat_id: int, db: Session):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat:
        cat.nickname = body.nickname
        cat.age = body.age
        cat.vaccinated = body.vaccinated
        cat.description = body.description
        cat.owner = body.owner_id
        db.commit()
    return cat


async def remove_cat(cat_id: int, db: Session):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat:
        db.delete(cat)
        db.commit()
    return cat


async def set_vaccinated(body: PetStatusVaccinated, cat_id: int, db: Session):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat:
        cat.vaccinated = body.vaccinated
        db.commit()
    return cat
