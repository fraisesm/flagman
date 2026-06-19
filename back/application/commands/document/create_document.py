from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateDocumentCommand:
    title: str
    content: str
    sender_user_id: int
    organization_id: int
    department_id: Optional[int] = None
    link: Optional[str] = None
