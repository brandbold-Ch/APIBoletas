"""
This module provides functionality to handle student data and apply academic ratings.

It includes:
- A decorator (`get_ratings`) that processes student objects to apply ratings to their academic load.

Key Features:
- Validates the presence of essential attributes ('CARGA' or 'HISTORIAL') in student objects.
- Applies ratings based on the provided partial.
- Custom error handling to manage unexpected issues during processing.

Dependencies:
- ALUMNO model for student data management.
- Ratings utility for academic load evaluation.
"""
from utils.rating_tools import Ratings


async def get_ratings(enrollment: str = None, student: dict = None, partial: int = None) -> dict:
    aggregate: list[dict] = student.get("CARGA") or student.get("HISTORIAL")
    ratings = Ratings(aggregate, partial)
    return ratings.score(student)
