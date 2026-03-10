from fastapi import APIRouter
from app.services.data_service import insert_record, get_records

router = APIRouter()


@router.post("/{table_name}")
def insert_data(table_name: str, data: dict):

    return insert_record(table_name, data)


@router.get("/{table_name}")
def read_data(table_name: str):

    return get_records(table_name)