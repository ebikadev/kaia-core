from pydantic import BaseModel
from typing import List, Dict


class ValidationResult(BaseModel):

    valid: bool
    row_count: int
    columns_detected: List[str]
    missing_columns: List[str]
    unexpected_columns: List[str]
    null_values: Dict[str, int]