"""
CSV Service

Handles CSV parsing and returns rows as dictionaries.
"""

import csv
from io import StringIO


def parse_csv(file_content: str):

    reader = csv.DictReader(StringIO(file_content))

    rows = []

    for row in reader:
        rows.append(row)

    return rows