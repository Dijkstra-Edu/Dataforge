from typing import Optional
from datetime import date


def calculate_months_served(
    start_month: int,
    start_year: int,
    end_month: Optional[int],
    end_year: Optional[int]
) -> int:

    # If no end date, assume ongoing → use today
    if end_month is None or end_year is None:
        today = date.today()
        end_month = today.month
        end_year = today.year

    # Convert dates into total months
    start_total = start_year * 12 + start_month
    end_total = end_year * 12 + end_month

    months = end_total - start_total

    # Ensure non-negative result (if data is wrong)
    return max(months, 0)