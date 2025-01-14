from flask import Flask, Blueprint, request, jsonify
from datetime import date, datetime, time, timedelta
from sqlalchemy.orm import Session
from database import engine, OperatorsAvailability, Operator, Laboratory

app = Flask(__name__)

# funzione per gestire l'aggiunta di minuti ad un oggetto time. non è necessario gestire il giorno successivo
def add_minutes_to_time(original_time, minutes_to_add):
    temp_datetime = datetime.combine(date.today(), original_time)
    temp_datetime += timedelta(minutes=minutes_to_add)
    return temp_datetime.time()

#funzione per verificare se uno slot è già stato prenotato
def slot_is_booked(slot, booked_slots):
    for booked_slot in booked_slots:
        if slot["operator_availability_id"] == booked_slot["operator_availability_id"] and slot["operator_availability_date"] == booked_slot["booked_slot_date"] and slot["operator_availability_slot_start"] == booked_slot["booked_slots_slot_start"] and slot["operator_availability_slot_end"] == booked_slot["booked_slots_slot_end"]:
            return True
    return False

#funzione per verificare se uno slot è in un periodo di chiusura di un laboratorio 
def lab_is_closed(slot, laboratory_closures):
    for laboratory_closure in laboratory_closures:
        if slot["laboratory_id"] == laboratory_closure["laboratory_id"]:
            if datetime.combine(slot["operator_availability_date"],slot["operator_availability_slot_start"]) < laboratory_closure["end_datetime"] and datetime.combine(slot["operator_availability_date"],slot["operator_availability_slot_end"]) > laboratory_closure["start_datetime"]:
                return True
    return False

#funzione per verificare se uno slot è in un periodo di assenza di un operatore 
def operator_is_absent(slot, operator_absences):
    for operator_absence in operator_absences:
        if slot["operator_id"] == operator_absence["operator_id"]:
            if datetime.combine(slot["operator_availability_date"],slot["operator_availability_slot_start"]) < operator_absence["end_datetime"] and datetime.combine(slot["operator_availability_date"],slot["operator_availability_slot_end"]) > operator_absence["start_datetime"]:
                return True
    return False

#funzione per generare slot prenotabili a partire dalle disponibilità degli operatori datetime_from_filter viene utilizzato come parametro nella route per non fornire date nel passato
def generate_availabile_slots(operators_availability, datetime_from_filter = None, laboratory_closures = None, operator_absences = None, booked_slots = None):
    # definizione dell'array che coneterrà gli slot generati
    operators_availability_slots = []
    # esamina ogni operator_availability rule
    for operator_availability in operators_availability:
        # se datetime_from_filter è impostato filtra la disponibilià degli esami partendo da quella data (se maggiore)
        if  isinstance(datetime_from_filter, datetime) and datetime_from_filter.date() > operator_availability.available_from_date:
            operator_availability_date = datetime_from_filter.date()
        else:
            operator_availability_date = operator_availability.available_from_date
        # sposta operator_availability date al primo giorno della settimana indicato nella operator_availability
        operator_availability_date += timedelta(days=((operator_availability.available_weekday - operator_availability_date.weekday()) % 7))
        # per ciascun giorno fino a fine disponibilià compresa 
        while operator_availability_date <= operator_availability.available_to_date:
            # imposta la partenza del primo slot sempre all'orario di partenza delle disponibiltà
            operator_availability_slot_start = operator_availability.available_from_time
            # per ciascun giorno crea gli slot in fino all'ora di di fine disponibilità
            while operator_availability_slot_start < operator_availability.available_to_time:
                # calcola la fine dello slot
                operator_availability_slot_end = add_minutes_to_time(operator_availability_slot_start, operator_availability.slot_duration_minutes)
                # se lo slot supera l'orario esci e passa alla settimana successiva
                if operator_availability_slot_end > operator_availability.available_to_time:
                   break
                
                # crea lo slot come oggetto dictonary
                slot = {
                    "operator_availability_id": operator_availability.availability_id,
                    "exam_type_id": operator_availability.exam_type_id,
                    "exam_type_name": operator_availability.exam_type_id,
                    "laboratory_id":operator_availability.laboratory_id,
                    "laboratory_name": operator_availability.laboratory.name,
                    "operator_name": operator_availability.operator.operator_name,
                    "operator_availability_date":  operator_availability_date.isoformat(),
                    "operator_availability_slot_start": operator_availability_slot_start.isoformat(),
                    "operator_availability_slot_end": operator_availability_slot_end.isoformat()
                }

                # se lo slot è dopo l'orario del filtro e se è il laboratorio non è chiuso l'oepratore in ferie e lo slot non è già prenotato
                if (
                    ((datetime_from_filter == None) or (datetime.combine(operator_availability_date, operator_availability_slot_start) >= datetime_from_filter)) and
                    ((laboratory_closures == None) or (not lab_is_closed(slot,laboratory_closures))) and 
                    ((operator_absences == None) or (not operator_is_absent(slot,operator_absences))) and 
                    ((booked_slots == None) or (not slot_is_booked(slot,booked_slots)))):
                    
                    # aggiungi lo slot all'array
                    operators_availability_slots.append(slot)

                #passa allo slot successivo
                operator_availability_slot_start = add_minutes_to_time(operator_availability_slot_end, operator_availability.pause_minutes)
            # passa alla settimana successiva
            operator_availability_date += timedelta(days=7)

    return operators_availability_slots

@slots_bp.route('/api/slots_availability', methods=['GET'])
def get_slots_availability():
    # Restituisci le disponibilità da una data specifca
    datetime_from_filter = request.args.get('datetime_from_filter')
    # Restituisci le disponibilità di un esame specifico
    exam_type_id = request.args.get('exam_type_id', type=int)
    # Restituisci le disponibilità di un operatore specifico
    operator_id = request.args.get('operator_id', type=int)
    # Restituisci le disponibilità di un laboratorio specifico
    laboratory_id = request.args.get('laboratory_id', type=int)

    # Imposta un controllo sulla data di partenza della verifica delle disponibilità che non può essere nel passato o nel giorno corrente
    # può essere richiesta la disponibità dalla data successiva alla data odierna
    first_reservation_datetime = datetime.combine(datetime.now().date() + timedelta(days=1), time(0, 6))
    if datetime_from_filter:
        try:
            # Recupera la data di partenza delle disponibilità richiesta dall'utente e rimuovi l'ora
            datetime_from_filter = datetime.strptime(datetime_from_filter, '%Y-%m-%d %H:%M:%S').date()
            if datetime_from_filter.date() <= datetime.now().date():
                datetime_from_filter = first_reservation_datetime
        except ValueError:
            return jsonify({"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}), 400
    else:
        datetime_from_filter = first_reservation_datetime

    # tramite la sessione crea la query
    with Session(engine) as session:
        query = (
            session.query(OperatorsAvailability)
            .join(OperatorsAvailability.operator)
            .join(OperatorsAvailability.laboratory)
        )

        # Filtra la query in base ai parametri obbligatori la disponibilità deve essere attiva e non deve essere scaduta
        query = query.filter(OperatorsAvailability.enabled == True)
        query = query.filter(OperatorsAvailability.available_to_date >= datetime_from_filter.date())

        # Filtra la query in base ai parametri opzionali
        if exam_type_id:
            query = query.filter(OperatorsAvailability.exam_type_id == exam_type_id)
        if operator_id:
            query = query.filter(OperatorsAvailability.operator.operator_id == operator_id)
        if laboratory_id:
            query = query.filter(OperatorsAvailability.laboratory.laboratory_id == laboratory_id)

        results = query.all()

        for availability in results:
            print(
                "Availability ID:", availability.availability_id,
                "| Operator:", availability.operator.operator_name,
                "| Laboratory:", availability.laboratory.name
            )
        
        try:
            slots = get_operator_availabilitys_slots(results, datetime_from_filter)
            return jsonify(slots), 200
        except Exception as e:
            # Log dell'errore con stack trace
            logging.error("Error in slot conversion: %s", str(e))
            logging.error(traceback.format_exc())
            return jsonify({"error": "Slot conversion Error"}), 500
        


