Event Management System 🎉
A comprehensive Event Management System built with Flask that allows users to register, log in, create events, and manage seat reservations. The system supports user authentication, event CRUD operations, and provides a profile page to view registered events.

📋 Table of Contents
Features
Tech Stack
Project Structure
Setup Instructions
Usage
Screenshots
Future Enhancements
Contributing

🚀 Features
User Authentication: Registration and login functionality with session management.
Event Management: Create, update, delete, and view events.
Seat Booking: Users can register for events with seat capacity limits.
Profile Management: Users can view their registered events in their profile.
Search Functionality: Search for events by name on the home page.
Responsive Design: Mobile-friendly layout for seamless user experience.

🛠️ Tech Stack
Technology	Description
Flask	Backend framework for handling routes and logic
SQLite	Lightweight database for storing user and event data
HTML/CSS	Frontend structure and styling
Jinja2	Templating engine for dynamic content

📂 Project Structure
text
project/
│
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page template
│   ├── profile.html        # Profile page template
│   ├── register.html       # Registration page template
│   ├── login.html          # Login page template
│   └── event_detail.html   # Event details template
│
├── static/                 # Static files (CSS, JS)
│   ├── css/
│   │   ├── style_base.css  # Shared styles across pages
│   │   ├── style_index.css # Styles specific to the home page
│   │   └── others.css      # Styles for other pages
│   └── js/
│       └── script.js       # Optional JavaScript file
│
├── database/               # Database files (SQLite)
│   └── event_management.db # SQLite database file
└── README.md               # Project documentation

⚙️ Setup Instructions
Prerequisites:
Python 3.x installed on your system.
Git installed on your system.

Steps to Run Locally:
Clone the repository:
git clone https://github.com/yourusername/event-management-system.git
cd event-management-system
Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:
pip install -r requirements.txt
Initialize the database:
python -c "from app import get_db_connection; conn = get_db_connection(); conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, name TEXT, surname TEXT);'); conn.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT, start_date DATE, end_date DATE, location TEXT, price REAL, quota INTEGER);'); conn.execute('CREATE TABLE IF NOT EXISTS participations (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, event_id INTEGER NOT NULL);'); conn.close();"
Run the application:
flask run
Open your browser and navigate to http://127.0.0.1:5000.

🖥️ Usage
Register a new user account on the registration page.
Log in using your credentials.
Create new events or browse existing ones.
Register for an event with available seats.
View your registered events in the profile section.

📸 Screenshots
Home Page:
Home Page

Profile Page:
Profile Page

🔮 Future Enhancements
Add real-time notifications using WebSockets (e.g., seat availability updates).
Implement email notifications for event registration confirmations.
Add admin functionality to manage users and events.
Add Machine learning Suggestion in search functionality.
Deploy the application using Docker or cloud platforms like AWS/GCP.

🤝 Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests.
Steps to Contribute:
Fork the repository.
Create a new branch (git checkout -b feature-name).
Commit your changes (git commit -m "Add some feature").
Push to the branch (git push origin feature-name).
Open a pull request.

