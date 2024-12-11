# **Project: Daily Help Services**

## **Overview**

The **Daily Help Services** project is a web application built using Flask that allows users to post and book services.  
- **Service Providers**: List their services.  
- **Clients**: Browse, view details, and book services.  

The application uses **Flask-SQLAlchemy** for database management and provides a clean, user-friendly interface.

---

## **Project Structure**

```plaintext
project/
├── app.py                     # Main Flask application file
├── static/                    # Static files (CSS, JavaScript, etc.)
│   ├── css/
│   │   └── style.css          # Stylesheet for the application
│   └── js/
│       └── main.js            # JavaScript functionality for the application
├── templates/                 # HTML templates for the application
│   ├── base.html              # Base template with shared layout
│   ├── index.html             # Homepage template
│   ├── services.html          # Page displaying all services
│   ├── new_service.html       # Form to post a new service
│   ├── service_detail.html    # Detailed view of a specific service
│   └── book_service.html      # Form to book a service
└── instance/                  # Instance folder for SQLite database
    └── services.db            # SQLite database file
```
## Installation Instructions

1.	Create a virtual environment:

        python -m venv venv


2.	Activate the virtual environment:
```
•	Windows:

venv\Scripts\activate

•	Mac/Linux:

source venv/bin/activate
```

3.	Install required packages:

        pip install flask flask-sqlalchemy


4.	Set up the project structure:
   
        Create the file structure as described in the Project Structure section.
6.	Add the files:
   
        Copy the respective code snippets provided in this README into the appropriate files in the project structure.

## Usage Instructions

1.	Run the application:

        python app.py


2.	Access the application:
   
        Open your browser and navigate to http://127.0.0.1:5000.
3.	Features:
   
        •	Homepage: View featured services.
        •	All Services: Browse all listed services.
        •	Post Service: Add a new service with details like title, description, price, provider name, and email.
        •	Service Detail: View detailed information about a service.
        •	Book Service: Book a service by providing your name, email, and preferred date.

## Code Snippets

### app.py

The main application script handles the routes, database models, and logic for service posting and booking. Ensure you set up the database correctly by running the following command:
```
with app.app_context():
    db.create_all()
```
### HTML Templates

Templates are stored in the templates/ directory. The base.html template serves as the base layout for all other pages.

### Static Files

	•	CSS: Styling for the application is located in static/css/style.css.
	•	JavaScript: Additional client-side functionality can be added in static/js/main.js.

## Example Workflow

	1.	Post a Service: Go to Post a Service and fill out the form to add a new service.
	2.	View Services: Navigate to the All Services page to see the listed services.
	3.	Book a Service: Select a service, view its details, and use the Book Now option to make a booking.

## Dependencies

	•	Flask
	•	Flask-SQLAlchemy

## Future Enhancements

	•	Add authentication for users.
	•	Integrate email notifications for service bookings.
	•	Implement service categories for better organization.
