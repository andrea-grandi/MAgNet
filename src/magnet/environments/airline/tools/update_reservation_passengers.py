"""Adapted from τ-bench https://arxiv.org/abs/2406.12045"""

import json
from typing import List, Dict, Any
from magnet.utils import get_data


def update_reservation_passengers(
    reservation_id: str,
    passengers: List[Dict[str, Any]],
) -> str:
    """
    Update the passenger information of a reservation.

    Args:
        reservation_id: The reservation ID, such as 'ZFA04Y'.
        passengers: An array of objects containing details about each passenger.
                   Each object should have 'first_name', 'last_name', and
                   'dob' properties.
                   The date of birth should be in the format 'YYYY-MM-DD'.

    Returns:
        A JSON string representing the updated reservation or an error message.
    """
    data = get_data()
    reservations = data["reservations"]
    if reservation_id not in reservations:
        return "Error: reservation not found"
    reservation = reservations[reservation_id]
    if len(passengers) != len(reservation["passengers"]):
        return "Error: number of passengers does not match"
    reservation["passengers"] = passengers
    return json.dumps(reservation)
