from flask import Flask, request, jsonify
from datetime import datetime, time, timedelta
from . import db
from .models import Exam, Laboratory_Closures, Operator_Absences, Bookings
app = Flask(__name__)

@app.route('/api/availability', methods=['GET'])
def get_availability():
    from_str = request.args.get('from')
    to_str = request.args.get('to')
    exam_type_id = request.args.get('exam_type_id', type=int)
    operator_id = request.args.get('operator_id', type=int)

    # Conversione date dellla query 
    from_date = datetime.strptime(from_str, "%Y-%m-%d").date() if from_str else None
    to_date = datetime.strptime(to_str, "%Y-%m-%d").date() if to_str else None

    # Impostazione Query con filtro in base alle date operatore e tipo esame (se impostati)
    query = db.session.query(Exam).filter(Exam.Is_Available == True)
    query = query.filter(Exam.Avaiable_From <= to_date and Exam.Avaiable_To >= from_date)
    
    if exam_type_id:
        query = query.filter(Exam.Exam_Type_ID == exam_type_id)
    if operator_id:
        query = query.filter(Exam.Operator_ID == operator_id)

    filtered_exams = query.all()  # Esecuzione Query
    """Rimuove gli slot già prenotati da Bookings."""
    if not slots:
        return slots

    # Troviamo i booking che toccano il range di date/ore degli slot
    min_dt = min(s["start"] for s in slots)
    max_dt = max(s["end"] for s in slots)

    # Query su Bookings: per semplicità assumiamo Appointment_Date in TIMESTAMP
    # e lo consideriamo come inizio dello slot
    bookings = db.session.query(Bookings).filter(
        Bookings.Exam_ID == exam_id,
        Bookings.Appointment_Date >= min_dt,
        Bookings.Appointment_Date < max_dt  # < se le prenotazioni durano slot_duration
    ).all()

    # Costruisci un set di date/ore prenotate
    booked_datetimes = []
    for b in bookings:
        start_b = b.Appointment_Date  # datetime
        end_b = start_b + timedelta(minutes=???)  # qui devi aggiungere la durata corrispondente
        booked_datetimes.append((start_b, end_b))

    def is_booked(slot):
        """Verifica se slot si sovrappone a una prenotazione."""
        for (start_b, end_b) in booked_datetimes:
            if slot["start"] < end_b and slot["end"] > start_b:
                return True
        return False

    return [s for s in slots if not is_booked(s)]

