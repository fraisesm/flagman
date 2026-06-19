from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.commands.document.create_document import CreateDocumentCommand
from application.commands.document.send_document import SendDocumentCommand
from application.commands.document.send_to_department import SendToDepartmentCommand
from application.commands.document.forward_document import ForwardDocumentCommand
from application.handlers.document.create_document_handler import CreateDocumentHandler
from application.handlers.document.send_document_handler import SendDocumentHandler
from application.handlers.document.send_to_department_handler import SendToDepartmentHandler
from application.handlers.document.forward_document_handler import ForwardDocumentHandler
from application.handlers.document.get_inbox_handler import GetInboxHandler
from application.handlers.document.get_outbox_handler import GetOutboxHandler
from application.handlers.document.get_pending_inbox_handler import GetPendingInboxHandler
from application.handlers.document.get_read_inbox_handler import GetReadInboxHandler
from application.handlers.document.get_signed_inbox_handler import GetSignedInboxHandler
from application.handlers.document.mark_as_read_handler import MarkAsReadHandler
from application.dependencies.auth import get_current_user
from application.dependencies.roles import require_boss_or_admin, require_employee
from data.db import get_db
from data.repositories.document_repository import DocumentRepository
from data.repositories.access_repository import AccessRepository
from data.repositories.employee_repository import EmployeeRepository
from data.repositories.signature_repository import SignatureRepository
from data.schemas.document import (
    CreateDocumentRequest,
    UpdateDocumentRequest,
    SendDocumentRequest,
    SendToDepartmentRequest,
    ForwardDocumentRequest,
    InboxRequest,
    OutboxRequest,
    DocumentResponse,
)

router = APIRouter(prefix="/documents", tags=["Documents"])


def _doc_dict(doc, status=None):
    d = {
        "document_id": doc.id,
        "title": doc.title,
        "content": doc.content,
        "link": doc.link,
        "sender_user_id": doc.sender_user_id,
        "organization_id": doc.organization_id,
        "department_id": doc.department_id,
    }
    if status is not None:
        d["status"] = status
    return d


# ---- Создание (boss / admin) ----

@router.post("/create", response_model=DocumentResponse)
def create_document(
    request: CreateDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_boss_or_admin),
):
    repo = DocumentRepository(db)
    handler = CreateDocumentHandler(repo)
    command = CreateDocumentCommand(
        title=request.title,
        content=request.content or "",
        link=request.link,
        sender_user_id=current_user.id,
        organization_id=request.organization_id,
        department_id=request.department_id,
    )
    try:
        return handler.handle(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/unread-count/{user_id}")
def get_unread_count(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = DocumentRepository(db)
    return {"unread_count": repo.get_unread_count(user_id)}


@router.get("/status/{document_id}/{recipient_user_id}")
def get_document_status(
    document_id: int,
    recipient_user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = DocumentRepository(db)
    status = repo.get_document_status_for_user(document_id, recipient_user_id)
    if not status:
        raise HTTPException(status_code=404, detail="Статус не найден")
    return status


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = DocumentRepository(db)
    doc = repo.get_by_id(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return doc


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: int,
    request: UpdateDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_boss_or_admin),
):
    repo = DocumentRepository(db)
    doc = repo.get_by_id(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    if doc.sender_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    doc.title = request.title
    doc.content = request.content
    doc.link = request.link
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_boss_or_admin),
):
    repo = DocumentRepository(db)
    doc = repo.get_by_id(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Документ не найден")
    if doc.sender_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    repo.delete(document_id)
    return {"detail": "Документ удалён"}


# ---- Отправка (boss / admin) ----

@router.post("/send")
def send_document(
    request: SendDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_boss_or_admin),
):
    handler = SendDocumentHandler(
        document_repository=DocumentRepository(db),
        access_repository=AccessRepository(db),
        employee_repository=EmployeeRepository(db),
    )
    command = SendDocumentCommand(
        document_id=request.document_id,
        sender_user_id=current_user.id,
        organization_id=request.organization_id,
        department_id=request.department_id,
        recipient_user_id=request.recipient_user_id,
    )
    try:
        recipient = handler.handle(command)
        return {
            "id": recipient.id,
            "document_id": recipient.document_id,
            "recipient_user_id": recipient.recipient_user_id,
            "status": recipient.status,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/send-to-department")
def send_to_department(
    request: SendToDepartmentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_boss_or_admin),
):
    handler = SendToDepartmentHandler(
        document_repository=DocumentRepository(db),
        access_repository=AccessRepository(db),
        employee_repository=EmployeeRepository(db),
    )
    command = SendToDepartmentCommand(
        document_id=request.document_id,
        sender_user_id=current_user.id,
        organization_id=request.organization_id,
        department_id=request.department_id,
    )
    try:
        recipients = handler.handle(command)
        return {
            "sent_to": len(recipients),
            "recipients": [
                {"id": r.id, "recipient_user_id": r.recipient_user_id, "status": r.status}
                for r in recipients
            ],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---- Пересылка (employee / admin) ----

@router.post("/forward")
def forward_document(
    request: ForwardDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_employee),
):
    handler = ForwardDocumentHandler(
        document_repository=DocumentRepository(db),
        access_repository=AccessRepository(db),
        signature_repository=SignatureRepository(db),
    )
    command = ForwardDocumentCommand(
        document_id=request.document_id,
        sender_user_id=current_user.id,
        organization_id=request.organization_id,
        department_id=request.department_id,
        recipient_user_id=request.recipient_user_id,
    )
    try:
        recipient = handler.handle(command)
        return {
            "id": recipient.id,
            "document_id": recipient.document_id,
            "recipient_user_id": recipient.recipient_user_id,
            "status": recipient.status,
            "forwarded_by": current_user.id,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---- Ящики ----

@router.post("/inbox")
def get_inbox(request: InboxRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = DocumentRepository(db)
    items = GetInboxHandler(repo).handle(request.user_id)
    return [_doc_dict(doc, r.status) for r, doc in items]


@router.post("/outbox")
def get_outbox(request: OutboxRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = DocumentRepository(db)
    docs = GetOutboxHandler(repo).handle(request.user_id)
    return [_doc_dict(doc) for doc in docs]


@router.post("/pending")
def get_pending(request: InboxRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = DocumentRepository(db)
    items = GetPendingInboxHandler(repo).handle(request.user_id)
    return [_doc_dict(doc, r.status) for r, doc in items]


@router.post("/read-list")
def get_read_list(request: InboxRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = DocumentRepository(db)
    items = GetReadInboxHandler(repo).handle(request.user_id)
    return [_doc_dict(doc, r.status) for r, doc in items]


@router.post("/signed-list")
def get_signed_list(request: InboxRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = DocumentRepository(db)
    items = GetSignedInboxHandler(repo).handle(request.user_id)
    return [_doc_dict(doc, r.status) for r, doc in items]


@router.post("/mark-read/{document_id}")
def mark_as_read(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = DocumentRepository(db)
    return MarkAsReadHandler(repo).handle(document_id=document_id, user_id=current_user.id)
