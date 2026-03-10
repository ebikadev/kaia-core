"""
Validation Report Model
"""

from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime


class ValidationReport(BaseModel):

    id: str

    table_name: str

    timestamp: datetime

    rows_analyzed: int

    valid_rows: int

    invalid_rows: int

    schema_errors: List[Dict]

    row_errors: List[Dict]