from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.commands.document.create_document import CreateDocumentCommand
from application.commands.document.send_document import SendDocumentCommand
from application.handlers.document.create_document_handler import CreateDocumentHandler
from application.handlers.document.send_document_handler import SendDocumentHandler
from data.db import get_db
from data.repositories.access_repository import AccessRepository
from data.repositories.document_repository import DocumentRepository
from data.schemas.document import CreateDocumentRequest, SendDocumentRequest

from application.handlers.document.get_inbox_handler import GetInboxHandler
from application.handlers.document.get_outbox_handler import GetOutboxHandler
from data.schemas.document import (
    CreateDocumentRequest,
    SendDocumentRequest,
    InboxRequest,
    OutboxRequest,
)

from application.handlers.document.get_pending_inbox_handler import GetPendingInboxHandler

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/create")
def create_document(request: CreateDocumentRequest, db: Session = Depends(get_db)):
    repository = DocumentRepository(db)
    handler = CreateDocumentHandler(repository)

    command = CreateDocumentCommand(
        title=request.title,
        content=request.content,
        sender_user_id=request.sender_user_id,
        organization_id=request.organization_id,
        department_id=request.department_id,
    )

    document = handler.handle(command)

    return {
        "id": document.id,  # type: ignore
        "title": document.title,  # type: ignore
        "content": document.content,  # type: ignore
        "sender_user_id": document.sender_user_id,  # type: ignore
        "organization_id": document.organization_id,  # type: ignore
        "department_id": document.department_id,  # type: ignore
    }


@router.post("/send")
def send_document(request: SendDocumentRequest, db: Session = Depends(get_db)):
    document_repository = DocumentRepository(db)
    access_repository = AccessRepository(db)
    handler = SendDocumentHandler(document_repository, access_repository)

    command = SendDocumentCommand(
        document_id=request.document_id,
        sender_user_id=request.sender_user_id,
        organization_id=request.organization_id,
        department_id=request.department_id,
        recipient_user_id=request.recipient_user_id,
    )

    try:
        recipient = handler.handle(command)
        return {
            "id": recipient.id,  # type: ignore
            "document_id": recipient.document_id,  # type: ignore
            "recipient_user_id": recipient.recipient_user_id,  # type: ignore
            "status": recipient.status,  # type: ignore
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/inbox")
def get_inbox(request: InboxRequest, db: Session = Depends(get_db)):
    repository = DocumentRepository(db)
    handler = GetInboxHandler(repository)

    items = handler.handle(request.user_id)

    result = []
    for recipient, document in items:
        result.append(
            {
                "document_id": document.id,  # type: ignore
                "title": document.title,  # type: ignore
                "content": document.content,  # type: ignore
                "sender_user_id": document.sender_user_id,  # type: ignore
                "organization_id": document.organization_id,  # type: ignore
                "department_id": document.department_id,  # type: ignore
                "status": recipient.status,  # type: ignore
            }
        )

    return result


@router.post("/outbox")
def get_outbox(request: OutboxRequest, db: Session = Depends(get_db)):
    repository = DocumentRepository(db)
    handler = GetOutboxHandler(repository)

    documents = handler.handle(request.user_id)

    result = []
    for document in documents:
        result.append(
            {
                "document_id": document.id,  # type: ignore
                "title": document.title,  # type: ignore
                "content": document.content,  # type: ignore
                "sender_user_id": document.sender_user_id,  # type: ignore
                "organization_id": document.organization_id,  # type: ignore
                "department_id": document.department_id,  # type: ignore
            }
        )

    return result


@router.get("/status/{document_id}/{recipient_user_id}")
def get_document_status(
    document_id: int,
    recipient_user_id: int,
    db: Session = Depends(get_db),
):
    repository = DocumentRepository(db)
    status = repository.get_document_status_for_user(document_id, recipient_user_id)

    if not status:
        raise HTTPException(status_code=404, detail="Статус документа не найден")

    return status   

@router.post("/pending")
def get_pending_documents(request: InboxRequest, db: Session = Depends(get_db)):
    repository = DocumentRepository(db)
    handler = GetPendingInboxHandler(repository)

    items = handler.handle(request.user_id)

    result = []
    for recipient, document in items:
        result.append(
            {
                "document_id": document.id,  # type: ignore
                "title": document.title,  # type: ignore
                "content": document.content,  # type: ignore
                "sender_user_id": document.sender_user_id,  # type: ignore
                "organization_id": document.organization_id,  # type: ignore
                "department_id": document.department_id,  # type: ignore
                "status": recipient.status,  # type: ignore
            }
        )

    return result