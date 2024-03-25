from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

password = os.getenv("PASSWORD")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@172.30.4.153:6000/postgres'
db = SQLAlchemy(app)

class SeatData_1(db.Model):
    __tablename__ = 'querynumber_1'
    id = db.Column(db.Integer, primary_key=True)
    occupied_column = db.Column(db.Float, nullable=False)
    available_column = db.Column(db.Float, nullable=False)
    timestamp_column = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'<SeatData_1 id:{self.id}, occupied_column:{self.occupied_column}, available_column:{self.available_column}, timestamp_column:{self.timestamp_column}>'

class SeatData_2(db.Model):
    __tablename__ = 'querynumber_2'
    id = db.Column(db.Integer, primary_key=True)
    occupied_column = db.Column(db.Float, nullable=False)
    available_column = db.Column(db.Float, nullable=False)
    timestamp_column = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f'<SeatData_2 id:{self.id}, occupied_column:{self.occupied_column}, available_column:{self.available_column}, timestamp_column:{self.timestamp_column}>'

@app.after_request
def add_charset(response):
    response.headers['Content-Type'] += '; charset=utf-8'
    return response

@app.route('/')
def index():
    return render_template("index.htm")

@app.route('/query')
def seat_query():
    latest_seat_data_1 = SeatData_1.query.order_by(SeatData_1.timestamp_column.desc()).first()
    latest_seat_data_2 = SeatData_2.query.order_by(SeatData_2.timestamp_column.desc()).first()

    if latest_seat_data_1 is not None:
        timestamp_1 = latest_seat_data_1.timestamp_column
    else:
        timestamp_1 = None

    if latest_seat_data_2 is not None:
        timestamp_2 = latest_seat_data_2.timestamp_column
    else:
        timestamp_2 = None
    def format_timestamp(timestamp):
        if timestamp is not None:
            return timestamp.strftime("%m-%d %H:%M")
        else:
            return None

    if request.headers.get('Accept') == 'application/json':
        if latest_seat_data_1 and latest_seat_data_2:
            total_value_1 = latest_seat_data_1.occupied_column + latest_seat_data_1.available_column
            available_value_1 = latest_seat_data_1.available_column

            total_value_2 = latest_seat_data_2.occupied_column + latest_seat_data_2.available_column
            available_value_2 = latest_seat_data_2.available_column

            data = {
                'all_available_value': available_value_1 + available_value_2,
                'all_total_value': total_value_1 + total_value_2,

                'floor1_available_value': available_value_1,
                'floor1_total_value': total_value_1,

                'floor2_available_value': available_value_2,
                'floor2_total_value': total_value_2,

                'timestamp_1': format_timestamp(timestamp_1),
                'timestamp_2': format_timestamp(timestamp_2)
            }
            return jsonify(data)

        else:
            return jsonify({'error': 'No seat data available'}), 404
    else:
        return render_template("seat_query.htm")

@app.route('/information')
def related_information():
    return render_template('related_information.htm')

@app.route('/recommendation')
def books_recommendation():
    return render_template('books_recommendation.htm')

@app.route('/update_data_1', methods=['POST'])
def update_data_1():
    data = request.json
    available_input = data.get('available')
    occupied_input = data.get('occupied')

    if available_input is not None and occupied_input is not None:
        seat_data = SeatData_1(occupied_column=occupied_input, available_column=available_input)
        db.session.add(seat_data)
        db.session.commit()
        print('Data updated successfully')
        return jsonify({'message': 'Data updated successfully'}), 200
    else:
        print("Invalid data provided")
        return jsonify({'error': 'Invalid data provided'}), 400

@app.route('/update_data_2', methods=['POST'])
def update_data_2():
    data = request.json
    available_input = data.get('available')
    occupied_input = data.get('occupied')

    if available_input is not None and occupied_input is not None:
        seat_data = SeatData_2(occupied_column=occupied_input, available_column=available_input)
        db.session.add(seat_data)
        db.session.commit()
        print('Data updated successfully')

        return jsonify({'message': 'Data updated successfully'}), 200
    else:
        print("Invalid data provided")
        return jsonify({'error': 'Invalid data provided'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)