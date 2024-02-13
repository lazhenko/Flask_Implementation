import unittest
from microservice_weather import app, db
from models import Temperature
from datetime import datetime, timedelta
from config import Config

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_temperature.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_temperature_history(self):
        # Mocking a temperature record
        record = Temperature(city="Kyiv", temperature=25.0, timestamp=datetime.utcnow())
        with app.app_context():
            db.session.add(record)
            db.session.commit()

        # Correct x-token and date format
        response = self.app.get('/temperature-history?day=' + datetime.now().strftime('%Y-%m-%d'),
                                headers={"x-token": Config.X_TOKEN})
        self.assertEqual(response.status_code, 200)

        # Invalid x-token
        response = self.app.get('/temperature-history?day=' + datetime.now().strftime('%Y-%m-%d'),
                                headers={"x-token": "wrongtoken"})
        self.assertEqual(response.status_code, 403)

        # Invalid date format
        response = self.app.get('/temperature-history?day=invalid-date',
                                headers={"x-token": Config.X_TOKEN})
        self.assertEqual(response.status_code, 400)

    # Add more tests as needed for other functionalities

if __name__ == '__main__':
    unittest.main()
