from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.scrap_item import ScrapItem
from app.schemas.scrap_item import ScrapItemCreate, ScrapItemRead, ScrapItemUpdate

router = APIRouter(prefix="/scrap", tags=["scrap"])


@router.get("/items", response_model=list[ScrapItemRead])
def list_scrap_items(db: Session = Depends(get_db)) -> list[ScrapItem]:
    return db.query(ScrapItem).filter(ScrapItem.is_archived == False).all()


@router.get("/items/{item_id}", response_model=ScrapItemRead)
def get_scrap_item(item_id: int, db: Session = Depends(get_db)) -> ScrapItem:
    item = db.query(ScrapItem).filter(ScrapItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scrap item not found")
    return item


@router.post("/items", response_model=ScrapItemRead, status_code=status.HTTP_201_CREATED)
def create_scrap_item(payload: ScrapItemCreate, db: Session = Depends(get_db)) -> ScrapItem:
    item = ScrapItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/items/{item_id}", response_model=ScrapItemRead)
def update_scrap_item(item_id: int, payload: ScrapItemUpdate, db: Session = Depends(get_db)) -> ScrapItem:
    item = db.query(ScrapItem).filter(ScrapItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scrap item not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scrap_item(item_id: int, db: Session = Depends(get_db)) -> None:
    item = db.query(ScrapItem).filter(ScrapItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scrap item not found")
    item.is_archived = True
    db.commit()
