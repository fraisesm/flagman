from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from application.handlers.signature.sign_document_handler import SignDocumentHandler
from application.dependencies.auth import get_current_user
from application.dependencies.roles import require_employee
from data.db import get_db
from data.repositories.signature_repository import SignatureRepository
from data.repositories.document_repository import DocumentRepository
from data.repositories.user_repository import UserRepository
from data.schemas.signature import SignDocumentRequest, SignatureResponse

router = APIRouter(prefix="/signatures", tags=["Signatures"])


@router.post("/sign", response_model=SignatureResponse)
def sign_document(
    request: SignDocumentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_employee),   # ← только employee / admin
):
    handler = SignDocumentHandler(
        signature_repository=SignatureRepository(db),
        document_repository=DocumentRepository(db),
        user_repository=UserRepository(db),
    )
    try:
        return handler.handle(user_id=current_user.id, document_id=request.document_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{document_id}", response_model=List[SignatureResponse])
def get_signatures(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repo = SignatureRepository(db)
    return repo.get_by_document(document_id)
