"""
Validation Report Service
"""

import uuid
from datetime import datetime

from app.models.validation_report import ValidationReport
from app.repositories.validation_repository import (
    save_report,
    get_report,
    get_all_reports,
    get_reports_by_table
)


def create_validation_report(table_name, validation_result):

    report = ValidationReport(

        id=str(uuid.uuid4()),

        table_name=table_name,

        timestamp=datetime.utcnow(),

        rows_analyzed=validation_result["rows_analyzed"],

        valid_rows=validation_result["valid_rows"],

        invalid_rows=validation_result["invalid_rows"],

        schema_errors=validation_result["schema_errors"],

        row_errors=validation_result["row_errors"]

    )

    save_report(report)

    return report


def fetch_report(report_id: str):

    return get_report(report_id)


def fetch_all_reports():

    return get_all_reports()


def fetch_reports_by_table(table_name: str):

    return get_reports_by_table(table_name)