"""Adapted from τ-bench https://arxiv.org/abs/2406.12045"""

import json
from magnet.utils import get_data


def get_reservation_details(reservation_id: str) -> str:
    """
    Get the details of a reservation.

    Args:
        reservation_id: The reservation id, such as '8JX2WO'.

    Returns:
        A JSON string representing the reservation details or an error message.
    """
    data = get_data()
    reservations = data["reservations"]
    if reservation_id in reservations:
        return json.dumps(reservations[reservation_id])
    return "Error: user not found"
