from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from config import Config
from models import db, Temperature
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
db.init_app(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

def fetch_and_store_temperature():
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={Config.CITY_NAME}&appid={Config.OPEN_WEATHER_MAP_API_KEY}&units=metric")
    data = response.json()
    temperature = data['main']['temp']
    new_record = Temperature(city=Config.CITY_NAME, temperature=temperature, timestamp=datetime.utcnow())
    db.session.add(new_record)
    db.session.commit()

@scheduler.task('interval', id='fetch_temp', hours=1, misfire_grace_time=900)
def scheduled_task():
    fetch_and_store_temperature()
    print("Fetched and stored temperature")

@app.route('/temperature-history', methods=['GET'])
def get_temperature_history():
    x_token = request.headers.get('x-token')
    if x_token != Config.X_TOKEN:
        return jsonify({"error": "Invalid x-token header"}), 403

    day = request.args.get('day')
    if not day:
        return jsonify({"error": "Day parameter is required"}), 400

    try:
        date = datetime.strptime(day, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid day format. Use Y-m-d format"}), 400

    temperatures = Temperature.query.filter(Temperature.timestamp.between(date, date + timedelta(days=1)), Temperature.city == Config.CITY_NAME).all()
    return jsonify([{"city": temp.city, "temperature": temp.temperature, "timestamp": temp.timestamp.isoformat()} for temp in temperatures])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    print("start")
