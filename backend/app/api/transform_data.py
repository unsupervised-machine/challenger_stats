# Might need to transform the data before storing it in db. Add functionality here as needed

from typing import Dict
from datetime import datetime


def add_timestamps(data: Dict, field: str) -> Dict:
    # Set the specified field to the current timestamp
    data[field] = datetime.now()
    return data

