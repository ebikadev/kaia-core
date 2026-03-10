from typing import Dict, List

data_db: Dict[str, List[dict]] = {}

def insert_row(table_name: str, row: dict):

    if table_name not in data_db:
        data_db[table_name] = []

    data_db[table_name].append(row)

    return row

def get_rows(table_name: str):

    return data_db.get(table_name, [])