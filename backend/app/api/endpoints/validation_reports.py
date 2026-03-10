from fastapi import APIRouter

from app.services.validation_service import (
    fetch_report,
    fetch_all_reports,
    fetch_reports_by_table
)

router = APIRouter(prefix="/validation-reports")

@router.get("/table/{table_name}")
def get_table_reports(table_name: str):

    return fetch_reports_by_table(table_name)


@router.get("/{report_id}")
def get_report(report_id: str):

    return fetch_report(report_id)


@router.get("/")
def get_reports():

    return fetch_all_reports()