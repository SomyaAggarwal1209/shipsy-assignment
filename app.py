import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'kim_jong_un')

base_dir = os.path.abspath(os.path.dirname(__file__))
sqlite_path = os.path.join(base_dir, "shipsy.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{sqlite_path}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    from models import User, Shipment  
    app.run(debug=True)