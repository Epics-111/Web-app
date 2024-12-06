# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'
db = SQLAlchemy(app)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    provider_name = db.Column(db.String(100), nullable=False)
    provider_email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    services = Service.query.order_by(Service.created_at.desc()).limit(6).all()
    return render_template('index.html', services=services)

@app.route('/services')
def services():
    services = Service.query.order_by(Service.created_at.desc()).all()
    return render_template('services.html', services=services)

@app.route('/service/new', methods=['GET', 'POST'])
def new_service():
    if request.method == 'POST':
        service = Service(
            title=request.form['title'],
            description=request.form['description'],
            price=float(request.form['price']),
            provider_name=request.form['provider_name'],
            provider_email=request.form['provider_email']
        )
        db.session.add(service)
        db.session.commit()
        flash('Service posted successfully!', 'success')
        return redirect(url_for('services'))
    return render_template('new_service.html')

@app.route('/service/<int:id>')
def service_detail(id):
    service = Service.query.get_or_404(id)
    return render_template('service_detail.html', service=service)

@app.route('/book/<int:service_id>', methods=['GET', 'POST'])
def book_service(service_id):
    service = Service.query.get_or_404(service_id)
    if request.method == 'POST':
        booking = Booking(
            service_id=service_id,
            client_name=request.form['client_name'],
            client_email=request.form['client_email'],
            booking_date=datetime.strptime(request.form['booking_date'], '%Y-%m-%d')
        )
        db.session.add(booking)
        db.session.commit()
        flash('Service booked successfully!', 'success')
        return redirect(url_for('service_detail', id=service_id))
    return render_template('book_service.html', service=service)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
