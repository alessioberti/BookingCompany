from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Booking Company API!"})

@app.route('/bookings', methods=['GET'])
def get_bookings():
    # Logic to get bookings
    return jsonify({"bookings": []})

@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    # Logic to create a new booking
    return jsonify({"message": "Booking created successfully!"}), 201

@app.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    # Logic to get a specific booking
    return jsonify({"booking": {}})

@app.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.get_json()
    # Logic to update a booking
    return jsonify({"message": "Booking updated successfully!"})

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    # Logic to delete a booking
    return jsonify({"message": "Booking deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
    def get_db_connection():
        conn = psycopg2.connect(
            dbname="your_db_name",
            user="your_db_user",
            password="your_db_password",
            host="your_db_host",
            port="your_db_port"
        )
        return conn

    @app.route('/bookings', methods=['GET'])
    def get_bookings():
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM bookings;')
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"bookings": bookings})

    @app.route('/bookings', methods=['POST'])
    def create_booking():
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO bookings (customer_name, room_number, check_in_date, check_out_date) VALUES (%s, %s, %s, %s) RETURNING id;',
            (data['customer_name'], data['room_number'], data['check_in_date'], data['check_out_date'])
        )
        booking_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Booking created successfully!", "booking_id": booking_id}), 201

    @app.route('/bookings/<int:booking_id>', methods=['GET'])
    def get_booking(booking_id):
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM bookings WHERE id = %s;', (booking_id,))
        booking = cursor.fetchone()
        cursor.close()
        conn.close()
        if booking is None:
            return jsonify({"message": "Booking not found"}), 404
        return jsonify({"booking": booking})

    @app.route('/bookings/<int:booking_id>', methods=['PUT'])
    def update_booking(booking_id):
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE bookings SET customer_name = %s, room_number = %s, check_in_date = %s, check_out_date = %s WHERE id = %s;',
            (data['customer_name'], data['room_number'], data['check_in_date'], data['check_out_date'], booking_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Booking updated successfully!"})

    @app.route('/bookings/<int:booking_id>', methods=['DELETE'])
    def delete_booking(booking_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookings WHERE id = %s;', (booking_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Booking deleted successfully!"})