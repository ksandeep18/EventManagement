# Event Management System 

An Event Management System built with Flask that allows users to register, log in, create events, and manage seat reservations.

---

## 📋 Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Setup Instructions](#setup-instructions)

---

## 🚀 Features
- User Authentication: Registration and login functionality with session management.
- Event Management: Create, update, delete, and view events. (CRUD operations only by admins)
- Seat Booking: Users can register for events with seat capacity limits.
- Profile Management: Users can view their registered events in their profile.
- Search Functionality: Users can search the events they registered easily.

---

## 🛠️ Tech Stack
| Technology  | Description                     |
|-------------|---------------------------------|
| Flask       | Backend framework              |
| SQLite      | Lightweight database           |
| HTML/CSS    | Frontend structure and styling |

---

## ⚙️ Setup Instructions

---

# Fork the repo

# Clone the repository:
https://github.com/ksandeep18/EventManagement.git

# Setup Virtual Environments:
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate Virtual Environments:
venv\scripts\activate

# Install dependencies:
pip install -r requirements.txt

# Intialize the database:
sqlite3 event_management.db < schema.sql

# Run the application:
flask run



