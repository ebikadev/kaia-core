from pydantic import BaseModel
from typing import List, Optional


class ValidationErrorDetail(BaseModel):
    """
    Represents a specific error found during validation.
    """

    column: Optional[str]
    error: str


class ValidationResult(BaseModel):
    """
    Complete result of the validation process returned by the API.
    """

    table: str
    rows: int
    errors: int
    details: List[ValidationErrorDetail]