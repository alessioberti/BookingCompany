from datetime import date, datetime, time, timedelta

# funzione per gestire l'aggiunta di minuti ad un oggetto time. non è necessario gestire il giorno successivo
def add_minutes_to_time(original_time, minutes_to_add):
    temp_datetime = datetime.combine(date.today(), original_time)
    temp_datetime += timedelta(minutes=minutes_to_add)
    return temp_datetime.time()

# funzione per estrarre i giorni di esame dalle rule e da ogni giorno estrarre gli slot prenotabili
def get_exams_slots(exam_rules, datetime_from_filter=None, booked_slots=None, lab_closures=None, operator_absences=None):

    # definizione dell'array che coneterrà gli slot generati
    exams_slots = []

    # esamina ogni exam rule
    for exam in exam_rules:
        
        # prepara filtro su chiusure laboratori e assenze operatori filtra in base all'operatore e al laboratorio dell'esame
        if lab_closures:
            exam_lab_closures = [lab_closure for lab_closure in lab_closures if lab_closure.laboratory_id == exam.laboratory_id]
        else:
            exam_lab_closures = []
        if operator_absences:
            exam_operator_absences = [operator_absence for operator_absence in operator_absences if operator_absence.operator_id == exam.operator_id]
        else:
            exam_operator_absences = []

        # se datetime_from_filter è impostato filtra la disponibilià degli esami partendo da quella data (se maggiore)
        if isinstance(datetime_from_filter, datetime) and datetime_from_filter.date() > exam.available_from :
            exam_date = datetime_from_filter.date()
        else:
            exam_date = exam.available_from

        # per ciascun giorno fino a fine disponibilià compresa 
        while exam_date <= exam.available_to:

            # Scarta i giorni fino ad arrivare al giorno della exam rule
            if exam_date.weekday() != exam.weekday:
                exam_date += timedelta(days=1)
                continue

            exam_slot_start = exam.opening_time

            # per ciascun giorno crea gli slot in mase alla exam rule
            while exam_slot_start < exam.closing_time:
                
                # calcola la fine dello slot
                exam_slot_end = add_minutes_to_time(exam_slot_start, exam.slot_duration)

                # Filtra e scarta lo slot se:
                if (

                    # se il filtro datetime_from_filter impostato scarta gli slot nella data indicata in modo che gli slot partano da dalla data e ora del filtro 
                    (isinstance(datetime_from_filter, datetime) and exam_date == datetime_from_filter.date() and exam_slot_start < datetime_from_filter.time())  or
                    
                    # lo slot del laboratorio è in quando il laborario è chiuso
                    (lab_closures and any(lab_closure.start_date <= exam_slot_start <= lab_closure.end_date for lab_closure in exam_lab_closures)) or
                    (lab_closures and any(lab_closure.start_date <= exam_slot_end <= lab_closure.end_date for lab_closure in exam_lab_closures)) or

                    # l'operatore è in ferie 
                    (operator_absences and any(operator_absence.start_date <= exam_slot_start <= operator_absence.end_date for operator_absence in exam_operator_absences)) or
                    (operator_absences and any(operator_absence.start_date <= exam_slot_end <= operator_absence.end_date for operator_absence in exam_operator_absences)) or
                    
                    # è già prenotato 
                    (booked_slots and (exam.exam_id,exam_date,exam_slot_start,exam_slot_end in booked_slots))):
                
                        # passa allo slot successivo impostatdo la data di fine come data di inizio
                        exam_slot_start = exam_slot_end + add_minutes_to_time(exam_slot_start, exam.buffer_time)
                        continue

                # se lo slot supera l'orario di chisura esci per passare al giorno successivo
                if exam_slot_end > exam.closing_time:
                    break
                
                # general lo slot
                exam_slot = {
                    "exam_id": exam.exam_id,
                    "name": exam.name, 
                    "description": exam.description,
                    "exam_type_id": exam.exam_type_id,
                    "laboratory_id": exam.laboratory_id,
                    "operator_id": exam.operator_id,
                    "exam_date":  exam_date,
                    "exam_slot_start": exam_slot_start,
                    "exam_slot_end": exam_slot_end
                }

                # aggiungilo all'array
                exams_slots.append(exam_slot)

                # passa allo slot successivo impostatdo la data di fine come data di inizio
                #aggiungi una pausa se prevista se non prevista buffer_time sarà di 0 minuti
                exam_slot_start = exam_slot_end + add_minutes_to_time(exam_slot_start, exam.buffer_time)

            # passa alla settimana successiva
            exam_date += timedelta(days=7)

    return exams_slots

