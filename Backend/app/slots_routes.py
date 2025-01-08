from flask import Flask, request, jsonify
from datetime import date, datetime, time, timedelta
from . import db
from .models import Exam, Laboratory_Closures, Operator_Absences, Bookings
app = Flask(__name__)


   #funzione per generare slot prenotabili a partire dalle exam rules
def get_exams_slots(exams_query, datetime_from_filter):

   # funzione per gestire l'aggiunta di minuti ad un oggetto time. non è necessario gestire il giorno successivo
   def add_minutes_to_time(original_time, minutes_to_add):
       
       temp_datetime = datetime.combine(date.today(), original_time)
       temp_datetime += timedelta(minutes=minutes_to_add)
       return temp_datetime.time()
   
    # definizione dell'array che coneterrà gli slot generati
    exams_slots = []
    # esamina ogni exam rule
    for exam in exams_query:
       # se datetime_from_filter è impostato filtra la disponibilià degli esami partendo da quella data (se maggiore)
        if isinstance(datetime_from_filter, datetime) and datetime_from_filter.date() > exam.available_from:
            exam_date = datetime_from_filter.date()
        else:
            exam_date = exam.available_from_date
        # sposta exam date al primo giorno della settimana indicato nella exam rule
        exam_date += timedelta(days=((exam.available_weekday - exam_date.weekday()) % 7))
        # per ciascun giorno fino a fine disponibilià compresa 
        while exam_date <= exam.available_to_date:
           # imposta la partenza del primo slot sempre all'orario di partenza delle disponibiltà
           exam_slot_start = exam.available_from_time
           # per ciascun giorno crea gli slot in fino all'ora di di fine disponibilità
            while exam_slot_start < exam.available_to_time:
               # calcola la fine dello slot
               exam_slot_end = add_minutes_to_time(exam_slot_start, exam.slot_duration)
               # se lo slot supera l'orario esci per passare al giorno successivo
               if exam_slot_end > exam.available_to_time:
                   break
               # se il filtro datetime_from_filter impostato scarta lo slot se è dopo la data del filtro
               # passa allo slot successivo impostando l'orario di fine come data di inizio
                if isinstance(datetime_from_filter, datetime) and datetime.combine(exam_date, exam_slot_start) <= datetime_from_filter:
                   exam_slot_start = add_minutes_to_time(exam_slot_end, exam.pause_minutes)
                   continue
               # crea lo slot come oggetto dictonary
                exam_slot = {
                   "exam_id": exam.exam_id,
                   "name": exam.name, 
                   "description": exam.description,
                   "exam_type_id": exam.exam_type_id,
                   "laboratory_": exam.laboratory_name,
                   "operator_id": exam.operator_last_name,
                   "exam_date":  exam_date,
                   "exam_slot_start": exam_slot_start,
                   "exam_slot_end": exam_slot_end
               }
               # aggiungi lo slot all'array e passa allo slot successivo 
                exams_slots.append(exam_slot)
                exam_slot_start = add_minutes_to_time(exam_slot_end, exam.pause_minutes)
            # passa alla settimana successiva
            exam_date += timedelta(days=7)
    return exams_slots

@app.route('/api/slots_availability', methods=['GET'])
def get_slot_availability():
    datetime_from_filter = request.args.get('datetime_from_filter')
    if datetime_from_filter:
        try:
            datetime_from_filter = datetime.strptime(datetime_from_filter, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}), 400
    else:
        datetime_from_filter = None

    exams_query =   db.session.query(
                        Exam,Laboratory.name.label('laboratory_name'), Operator.first_name.label('operator_first_name'),Operator.last_name.label('operator_last_name')
                        ).join(Laboratory, Exam.laboratory_id == Laboratory.laboratory_id
                            ).join(Operator, Exam.operator_id == Operator.operator_id, isouter=True)
    
    # le prenotazioni sono disponibili sempre dal giorno successivo
    if datetime_from_filter (datetime_from_filter += datetime_from_filter += timedelta(days=1))

    try:
        slots = get_exams_slots(exams_query.all(), datetime_from_filter)
    except:
        return jsonify({"error": "Slot conversion Error"}), 500
    
    return jsonify(slots), 200