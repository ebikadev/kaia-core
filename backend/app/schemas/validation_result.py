from pydantic import BaseModel
from typing import List, Optional


class ValidationErrorDetail(BaseModel):
    """
    Representa un error específico encontrado durante la validación.
    """

    column: Optional[str]
    error: str


class ValidationResult(BaseModel):
    """
    Resultado completo del proceso de validación.
    """

    table: str
    rows: int
    errors: int
    details: List[ValidationErrorDetail]