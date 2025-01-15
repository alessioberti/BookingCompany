from datetime import datetime, timedelta

# Dati di esempio
operator_availability_slots = [
    {
        "operator_availability_id": 1,
        "exam_type_id": 2,
        "exam_type_name": "esami del sangue",
        "laboratory_id": 3,
        "laboratory_name": "Torino",
        "operator_name": "dott. Franco",
        "operator_availability_date": datetime(2025, 1, 2).isoformat(),
        "operator_availability_slot_start": datetime(2025, 1, 2, 9, 0).isoformat(),
        "operator_availability_slot_end": datetime(2025, 1, 2, 10, 0).isoformat(),
    },
    {
        "operator_availability_id": 1,
        "exam_type_id": 2,
        "exam_type_name": "esami del sangue",
        "laboratory_id": 3,
        "laboratory_name": "Torino",
        "operator_name": "dott. Franco",
        "operator_availability_date": datetime(2025, 1, 2).isoformat(),
        "operator_availability_slot_start": datetime(2025, 1, 2, 10, 0).isoformat(),
        "operator_availability_slot_end": datetime(2025, 1, 2, 11, 0).isoformat(),
    },
    {
        "operator_availability_id": 1,
        "exam_type_id": 2,
        "exam_type_name": "esami del sangue",
        "laboratory_id": 3,
        "laboratory_name": "Torino",
        "operator_name": "dott. Franco",
        "operator_availability_date": datetime(2025, 1, 2).isoformat(),
        "operator_availability_slot_start": datetime(2025, 1, 2, 11, 0).isoformat(),
        "operator_availability_slot_end": datetime(2025, 1, 2, 12, 0).isoformat(),
    },
]

slots_booked = [
    {
        "booked_slot_id": 1,
        "operator_availability_id": 1,
        "booked_slot_date": datetime(2025, 1, 2).isoformat(),
        "booked_slots_slot_start": datetime(2025, 1, 2, 9, 0).isoformat(),
        "booked_slots_slot_end": datetime(2025, 1, 2, 10, 0).isoformat(),
        "status": "rejected",
    },
    {
        "booked_slot_id": 2,
        "operator_availability_id": 1,
        "booked_slot_date": datetime(2025, 1, 2).isoformat(),
        "booked_slots_slot_start": datetime(2025, 1, 2, 10, 0).isoformat(),
        "booked_slots_slot_end": datetime(2025, 1, 2, 11, 0).isoformat(),
        "status": "confirmed",
    },
]


