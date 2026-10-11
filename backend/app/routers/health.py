from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project, ScrapItem
from app.schemas.project import ProjectCreate, ProjectOut
from app.schemas.scrap import ScrapItemCreate, ScrapItemOut

router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "ScrapMaster Unified"}


@router.get("/scrap/items", response_model=list[ScrapItemOut])
def list_scrap_items(db: Session = Depends(get_db)) -> list[ScrapItem]:
    return db.query(ScrapItem).all()


@router.post("/scrap/items", response_model=ScrapItemOut, status_code=status.HTTP_201_CREATED)
def create_scrap_item(payload: ScrapItemCreate, db: Session = Depends(get_db)) -> ScrapItem:
    if payload.project_id is not None:
        project = db.query(Project).filter(Project.id == payload.project_id).first()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

    item = ScrapItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)) -> list[Project]:
    return db.query(Project).all()


@router.post("/projects", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> Project:
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
