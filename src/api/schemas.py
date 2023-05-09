from pydantic import BaseModel


class DocumentData(BaseModel):
    document_type: str
    path: str