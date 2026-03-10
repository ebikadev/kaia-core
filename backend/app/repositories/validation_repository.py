"""
Validation Report Repository
"""

from typing import Dict
from app.models.validation_report import ValidationReport


validation_reports_db: Dict[str, ValidationReport] = {}


def save_report(report: ValidationReport):

    validation_reports_db[report.id] = report

    return report


def get_report(report_id: str):

    return validation_reports_db.get(report_id)


def get_all_reports():

    return list(validation_reports_db.values())


def get_reports_by_table(table_name: str):

    return [
        r for r in validation_reports_db.values()
        if r.table_name == table_name
    ]