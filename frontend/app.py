from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# Backend API URL (set via environment variable in Docker)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5000/api/data')

@app.route('/')
def index():
    try:
        response = requests.get(BACKEND_URL, timeout=3)
        data = response.json()
    except Exception as e:
        data = {"error": str(e)}
    
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)