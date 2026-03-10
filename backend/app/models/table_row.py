"""
    Request example:
        {
          "table_name": "countries",
          "data": {
            "id": 1,
            "name": "Argentina"
          }
        }

"""

from pydantic import BaseModel
from typing import Dict


class TableRow(BaseModel):
    """
    Represents a row inserted into a table.
    """
    table_name: str
    data: Dict