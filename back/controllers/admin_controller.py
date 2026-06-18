from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.handlers.admin.get_stats_handler import GetStatsHandler
from application.dependencies.roles import require_admin
from data.db import get_db
from data.repositories.stats_repository import StatsRepository
from data.repositories.document_repository import DocumentRepository

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Полная статистика для администратора:
    - всего документов / пользователей / организаций / отделов
    - документы по статусам (pending / read / signed)
    - пользователи по ролям (admin / boss / employee)
    """
    handler = GetStatsHandler(StatsRepository(db))
    return handler.handle()


@router.get("/documents")
def get_all_documents(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Все документы в системе — для администратора."""
    repo = StatsRepository(db)
    docs = repo.get_all_documents()
    return [
        {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "sender_user_id": doc.sender_user_id,
            "organization_id": doc.organization_id,
            "department_id": doc.department_id,
        }
        for doc in docs
    ]


@router.get("/signatures")
def get_recent_signatures(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Последние 20 подписей в системе."""
    repo = StatsRepository(db)
    return repo.get_recent_signatures()
