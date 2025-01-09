from flask import Flask, Blueprint, request, jsonify
from datetime import date, datetime, time, timedelta
from . import db
from .models import OperatorsAvailability, Laboratory, Operator  # Importa i modelli corretti
app = Flask(__name__)
import logging
import traceback

# funzione per gestire l'aggiunta di minuti ad un oggetto time. non è necessario gestire il giorno successivo
def add_minutes_to_time(original_time, minutes_to_add):
    temp_datetime = datetime.combine(date.today(), original_time)
    temp_datetime += timedelta(minutes=minutes_to_add)
    return temp_datetime.time()

   #funzione per generare slot prenotabili a partire dalle disponibilità degli operatori datetime_from_filter viene utilizzato come parametro nella route per non fornire date nel passato
def get_operator_availabilitys_slots(operators_availability, datetime_from_filter):
    # definizione dell'array che coneterrà gli slot generati
    operators_availability_slots = []
    # esamina ogni operator_availability rule
    for operator_availability in operators_availability:
        # se datetime_from_filter è impostato filtra la disponibilià degli esami partendo da quella data (se maggiore)
        if isinstance(datetime_from_filter, datetime) and datetime_from_filter.date() > operator_availability.available_from_date:
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
                # se lo slot supera l'orario esci per passare al giorno successivo
                if operator_availability_slot_end > operator_availability.available_to_time:
                   break
                # se il filtro datetime_from_filter impostato scarta lo slot se è dopo la data del filtro
                # passa allo slot successivo impostando l'orario di fine come data di inizio
                if isinstance(datetime_from_filter, datetime) and datetime.combine(operator_availability_date, operator_availability_slot_start) <= datetime_from_filter:
                    operator_availability_slot_start = add_minutes_to_time(operator_availability_slot_end, operator_availability.pause_minutes)
                    continue
                # crea lo slot come oggetto dictonary
                operator_availability_slot = {
                    "operator_availability_id": operator_availability.availability_id,
                    "exam_type_id": operator_availability.exam_type_id,
                    "laboratory_id": operator_availability.laboratory_id,
                    "operator_id": operator_availability.operator_id,
                    "operator_availability_date":  operator_availability_date.isoformat(),
                    "operator_availability_slot_start": operator_availability_slot_start.isoformat(),
                    "operator_availability_slot_end": operator_availability_slot_end.isoformat()
                }
                # aggiungi lo slot all'array e passa allo slot successivo 
                operators_availability_slots.append(operator_availability_slot)
                operator_availability_slot_start = add_minutes_to_time(operator_availability_slot_end, operator_availability.pause_minutes)
            # passa alla settimana successiva
            operator_availability_date += timedelta(days=7)

    return operators_availability_slots

slots_bp = Blueprint('slots', __name__)

@slots_bp.route('/api/slots_availability', methods=['GET'])
def get_slot_availability():
    
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

    # Costruisci una query sulla tabella operators_availability in join con laboratori e operatori
    operators_availability_query = db.session.query(OperatorsAvailability)

    # Filtra la query in base ai parametri obbligatori la disponibilità deve essere attiva e non deve essere scaduta
    
    operators_availability_query = operators_availability_query.filter(OperatorsAvailability.enabled == True)
    operators_availability_query = operators_availability_query.filter(OperatorsAvailability.available_to_date >= datetime_from_filter.date())

    # Filtra la query in base ai parametri opzionali
    if exam_type_id:
        operators_availability_query = operators_availability_query.filter(OperatorsAvailability.exam_type_id == exam_type_id)
    if operator_id:
        operators_availability_query = operators_availability_query.filter(OperatorsAvailability.operator_id == operator_id)
    if laboratory_id:
        operators_availability_query = operators_availability_query.filter(OperatorsAvailability.laboratory_id == laboratory_id)
    
    # Esegui la query
    try:
        operators_availability = operators_availability_query.all()
    except:
        return jsonify({"error": "Query error on table operators_availability"}), 500

    # Estrai gli slot dalle disponibilità degli operatori e restiusci un json
    try:
        slots = get_operator_availabilitys_slots(operators_availability, datetime_from_filter)
    except Exception as e:
        # Log dell'errore con stack trace
        logging.error("Error in slot conversion: %s", str(e))
        logging.error(traceback.format_exc())
        return jsonify({"error": "Slot conversion Error"}), 500
    
    return jsonify(slots), 200