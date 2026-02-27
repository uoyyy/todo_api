from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas, auth
from database import get_db
router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/{project_id}", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def created_task(
    project_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден или у вас нет к нему доступа")

    new_task = models.Task(**task.model_dump(), project_id=project_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
@router.get("/{project_id}", response_model=List[schemas.TaskResponse])
def get_tasks(
    project_id: int,
    is_completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден или у вас нет к нему доступа")
    query = db.query(models.Task).filter(models.Task.project_id == project_id)
    if is_completed is not None:
        query = query.filter(models.Task.is_completed == is_completed)
    return query.all()
@router.get("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_update: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена или нет доступа")

    for key, value in task_update.model_dump().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).join(models.Project).filter(
        models.Task.id == task_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена или нет доступа")
    db.delete(task)
    db.commit()
    return None