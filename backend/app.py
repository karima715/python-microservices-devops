from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Model
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

@app.route('/api/data')
def get_data():
    try:
        # Log the request
        logger.info("Backend API called")
        
        # Get data from database
        users = UserData.query.all()
        result = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Check if the UserData table is empty
        if UserData.query.count() == 0:
            # Add a default record with your name and email
            default_user = UserData(name="Karima Satkut", email="karimaji143@gmail.com")
            db.session.add(default_user)
            db.session.commit()
            logger.info("Default user added to the database")
    app.run(host='0.0.0.0', port=5000)