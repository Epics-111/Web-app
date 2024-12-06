# Required files structure:
"""
project/
    ├── app.py
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── js/
    │       └── main.js
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── services.html
    │   ├── new_service.html
    │   ├── service_detail.html
    │   └── book_service.html
    └── instance/
        └── services.db
"""

# Installation instructions:
"""
1. Create a new virtual environment:
   python -m venv venv

2. Activate the virtual environment:
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

3. Install required packages:
   pip install flask flask-sqlalchemy

4. Create the project structure as shown above

5. Copy the following files into their respective locations:
"""

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

# templates/base.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Daily Help Services{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header class="header">
        <h1>Daily Help Services</h1>
    </header>

    <nav class="nav">
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('services') }}">All Services</a>
        <a href="{{ url_for('new_service') }}">Post a Service</a>
    </nav>

    <main class="main">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>

# templates/index.html
{% extends "base.html" %}

{% block content %}
    <h2>Featured Services</h2>
    <div class="services-grid">
        {% for service in services %}
            {% include '_service_card.html' %}
        {% endfor %}
    </div>
{% endblock %}

# templates/_service_card.html
<div class="service-card">
    <h3>{{ service.title }}</h3>
    <p>{{ service.description }}</p>
    <div class="price">${{ "%.2f"|format(service.price) }}</div>
    <div class="provider-info">
        <p>Provider: {{ service.provider_name }}</p>
    </div>
    <a href="{{ url_for('service_detail', id=service.id) }}" class="btn">View Details</a>
</div>

# templates/services.html
{% extends "base.html" %}

{% block content %}
    <h2>All Services</h2>
    <div class="services-grid">
        {% for service in services %}
            {% include '_service_card.html' %}
        {% endfor %}
    </div>
{% endblock %}

# templates/new_service.html
{% extends "base.html" %}

{% block content %}
    <h2>Post a New Service</h2>
    <div class="form-container">
        <form method="POST">
            <div class="form-group">
                <label for="title">Service Title</label>
                <input type="text" id="title" name="title" required>
            </div>
            <div class="form-group">
                <label for="description">Description</label>
                <textarea id="description" name="description" required></textarea>
            </div>
            <div class="form-group">
                <label for="price">Price ($)</label>
                <input type="number" id="price" name="price" step="0.01" required>
            </div>
            <div class="form-group">
                <label for="provider_name">Your Name</label>
                <input type="text" id="provider_name" name="provider_name" required>
            </div>
            <div class="form-group">
                <label for="provider_email">Your Email</label>
                <input type="email" id="provider_email" name="provider_email" required>
            </div>
            <button type="submit" class="btn">Post Service</button>
        </form>
    </div>
{% endblock %}

# templates/service_detail.html
{% extends "base.html" %}

{% block content %}
    <div class="service-detail">
        <h2>{{ service.title }}</h2>
        <p class="description">{{ service.description }}</p>
        <div class="price">${{ "%.2f"|format(service.price) }}</div>
        <div class="provider-info">
            <p>Provider: {{ service.provider_name }}</p>
            <p>Contact: {{ service.provider_email }}</p>
        </div>
        <a href="{{ url_for('book_service', service_id=service.id) }}" class="btn">Book Now</a>
    </div>
{% endblock %}

# templates/book_service.html
{% extends "base.html" %}

{% block content %}
    <h2>Book Service: {{ service.title }}</h2>
    <div class="form-container">
        <form method="POST">
            <div class="form-group">
                <label for="client_name">Your Name</label>
                <input type="text" id="client_name" name="client_name" required>
            </div>
            <div class="form-group">
                <label for="client_email">Your Email</label>
                <input type="email" id="client_email" name="client_email" required>
            </div>
            <div class="form-group">
                <label for="booking_date">Preferred Date</label>
                <input type="date" id="booking_date" name="booking_date" required>
            </div>
            <button type="submit" class="btn">Book Service</button>
        </form>
    </div>
{% endblock %}

# static/css/style.css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
}

.header {
    background-color: #4CAF50;
    color: white;
    padding: 1rem;
    text-align: center;
}

.nav {
    background-color: #333;
    padding: 1rem;
    text-align: center;
}

.nav a {
    color: white;
    text-decoration: none;
    margin: 0 1rem;
    padding: 0.5rem 1rem;
    border-radius: 4px;
}

.nav a:hover {
    background-color: #555;
}

.main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.service-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.service-card h3 {
    margin-top: 0;
    color: #333;
}

.price {
    font-size: 1.25rem;
    font-weight: bold;
    color: #4CAF50;
    margin: 1rem 0;
}

.btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: #4CAF50;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    margin-top: 1rem;
}

.btn:hover {
    background-color: #45a049;
}

.provider-info {
    margin-top: 1rem;
    font-size: 0.9rem;
    color: #888;
}

.form-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.form-group textarea {
    height: 100px;
}

.alert {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 4px;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.service-detail {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

# static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Add any JavaScript functionality here
    console.log('Application loaded');
});

