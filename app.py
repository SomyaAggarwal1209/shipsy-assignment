import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change_this_secret')

base_dir = os.path.abspath(os.path.dirname(__file__))
sqlite_path = os.path.join(base_dir, "shipsy.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{sqlite_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Enum as SAEnum
import enum

class ShipmentStatus(enum.Enum):
    pending = "Pending"
    in_transit = "In-Transit"
    delivered = "Delivered"

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pw_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class Shipment(db.Model):
    __tablename__ = "shipments"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(SAEnum(ShipmentStatus), nullable=False, default=ShipmentStatus.pending)
    is_fragile = db.Column(db.Boolean, nullable=False, default=False)
    base_cost = db.Column(db.Float, nullable=False, default=0.0)
    tax_rate = db.Column(db.Float, nullable=False, default=0.0)
    handling_fee = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def total_cost(self):
        try:
            return round(self.base_cost * (1 + float(self.tax_rate)) + float(self.handling_fee), 2)
        except Exception:
            return None

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value if self.status else None,
            "is_fragile": self.is_fragile,
            "base_cost": self.base_cost,
            "tax_rate": self.tax_rate,
            "handling_fee": self.handling_fee,
            "total_cost": self.total_cost,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Choose a different one.", "warning")
            return redirect(url_for('register'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

from flask import abort

# List shipments with pagination + simple filter by status
@app.route('/shipments')
@login_required
def list_shipments():
    page = int(request.args.get('page', 1))
    per_page = 5
    status_filter = request.args.get('status')
    search_query = request.args.get('q')

    q = Shipment.query.order_by(Shipment.created_at.desc())

    if status_filter:
        try:
            enum_val = ShipmentStatus(status_filter)
            q = q.filter_by(status=enum_val)
        except Exception:
            pass

    if search_query:
        q = q.filter(Shipment.description.ilike(f"%{search_query}%"))

    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    return render_template(
        'shipments/list.html',
        pagination=pagination,
        status_filter=status_filter,
        search_query=search_query
    )

# View single shipment
@app.route('/shipments/<int:shipment_id>')
@login_required
def view_shipment(shipment_id):
    s = Shipment.query.get_or_404(shipment_id)
    return render_template('shipments/view.html', shipment=s)

# Create shipment 
@app.route('/shipments/create', methods=['GET', 'POST'])
@login_required
def create_shipment():
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        status = request.form.get('status', 'ShipmentStatus.pending')
        is_fragile = bool(request.form.get('is_fragile'))
        base_cost = float(request.form.get('base_cost') or 0)
        tax_rate = float(request.form.get('tax_rate') or 0)
        handling_fee = float(request.form.get('handling_fee') or 0)

        # map status string to enum safely
        try:
            status_enum = ShipmentStatus(request.form.get('status'))
        except Exception:
            status_enum = ShipmentStatus.pending

        s = Shipment(
            description=description,
            status=status_enum,
            is_fragile=is_fragile,
            base_cost=base_cost,
            tax_rate=tax_rate,
            handling_fee=handling_fee
        )
        db.session.add(s)
        db.session.commit()
        flash("Shipment created.", "success")
        return redirect(url_for('list_shipments'))
    return render_template('shipments/create.html', statuses=[st.value for st in ShipmentStatus])

# Edit shipment
@app.route('/shipments/<int:shipment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_shipment(shipment_id):
    s = Shipment.query.get_or_404(shipment_id)
    if request.method == 'POST':
        s.description = request.form.get('description', s.description)
        try:
            s.status = ShipmentStatus(request.form.get('status'))
        except Exception:
            pass
        s.is_fragile = bool(request.form.get('is_fragile'))
        s.base_cost = float(request.form.get('base_cost') or s.base_cost)
        s.tax_rate = float(request.form.get('tax_rate') or s.tax_rate)
        s.handling_fee = float(request.form.get('handling_fee') or s.handling_fee)
        db.session.commit()
        flash("Shipment updated.", "success")
        return redirect(url_for('view_shipment', shipment_id=s.id))
    return render_template('shipments/edit.html', shipment=s, statuses=[st.value for st in ShipmentStatus])

# Delete shipment
@app.route('/shipments/<int:shipment_id>/delete', methods=['POST'])
@login_required
def delete_shipment(shipment_id):
    s = Shipment.query.get_or_404(shipment_id)
    db.session.delete(s)
    db.session.commit()
    flash("Shipment deleted.", "info")
    return redirect(url_for('list_shipments'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)