from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional


def get_tasks(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = None,
        sort_order: str = "asc",
        status: Optional[schemas.TaskStatus] = None,
        priority: Optional[schemas.TaskPriority] = None,
        search: Optional[str] = None
) -> List[models.Task]:
    """Получение списка задач с возможностью сортировки и фильтрации"""
    query = db.query(models.Task)

    # Фильтрация
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if search:
        query = query.filter(
            (models.Task.title.ilike(f"%{search}%")) |
            (models.Task.description.ilike(f"%{search}%")))

        # Сортировка
        if sort_by:
            sort_field = {
                "title": models.Task.title,
                "status": models.Task.status,
                "created_at": models.Task.created_at,
                "priority": models.Task.priority
            }.get(sort_by, models.Task.created_at)

        if sort_order == "desc":
            sort_field = sort_field.desc()

        query = query.order_by(sort_field)

    return query.offset(skip).limit(limit).all()


def get_top_priority_tasks(db: Session, limit: int = 5) -> List[models.Task]:
    """Получение топ-N задач по приоритету"""
    return (
        db.query(models.Task)
            .order_by(models.Task.priority.desc(), models.Task.created_at.asc())
            .limit(limit)
            .all()
    )


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Получение одной задачи по ID"""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """Создание новой задачи"""
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
        db: Session,
        task_id: int,
        task: schemas.TaskCreate
) -> Optional[models.Task]:
    """Обновление существующей задачи"""
    db_task = get_task(db, task_id)
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Удаление задачи"""
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task