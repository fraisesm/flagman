from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.commands.signature.sign_document import SignDocumentCommand
from application.handlers.signature.sign_document_handler import SignDocumentHandler
from data.db import get_db
from data.repositories.access_repository import AccessRepository
from data.repositories.signature_repository import SignatureRepository
from data.schemas.signature import SignDocumentRequest

router = APIRouter(prefix="/signatures", tags=["Signatures"])


@router.post("/sign")
def sign_document(request: SignDocumentRequest, db: Session = Depends(get_db)):
    signature_repository = SignatureRepository(db)
    access_repository = AccessRepository(db)
    handler = SignDocumentHandler(signature_repository, access_repository)

    command = SignDocumentCommand(
        document_id=request.document_id,
        user_id=request.user_id,
        organization_id=request.organization_id,
        department_id=request.department_id,
        confirmation_channel=request.confirmation_channel,
    )

    try:
        signature = handler.handle(command)
        return {
            "id": signature.id,  # type: ignore
            "document_id": signature.document_id,  # type: ignore
            "user_id": signature.user_id,  # type: ignore
            "phone_signature": signature.phone_signature,  # type: ignore
            "confirmation_channel": signature.confirmation_channel,  # type: ignore
            "status": "signed",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))