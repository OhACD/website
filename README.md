# Personal Website Project

A Django-based personal website project aimed at building an advanced portfolio platform. Currently, the project focuses on backend development, with basic user authentication implemented.

---

## Table of Contents

- Overview
- Features
- Project Structure
- Installation
- Usage
- Future Development
- License

---

## Overview

This project is the foundation for a personal portfolio website. The backend currently supports:

- User registration and login
- Basic session-based authentication (login/logout)
- Protected index page that checks whether a user is logged in

The project is intended to be expanded into an interactive portfolio showcasing projects and personal achievements.

---

## Features

- User Authentication: Users can register, log in, and log out.
- Protected Index Page: `/main` checks if a user is logged in.
  - Logged-in users see `users.html` (confirmation they are authenticated).
  - Unauthenticated users are redirected to the login page.
- Basic Sessions: User authentication uses Django’s built-in sessions.
- Backend-Focused: Currently focuses on backend; frontend enhancements are planned.

---

## Project Structure

website/
├── my_website/
│   ├── main/              # Main App
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── main/
│   │   │       ├── layout.html
│   │   │       ├── login.html
│   │   │       ├── register.html
│   │   │       └── users.html
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── my_website/        # Default Django app folder
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── db.sqlite3          # local SQLite database (git-ignored)
├── .gitignore
└── README.md

- `main`: Custom app with endpoints, templates, and forms.
- `my_website`: Default Django project folder (settings, URLs, WSGI).
- `db.sqlite3`: Local SQLite database (git-ignored).

---

## Installation

1. Clone the repository

   git clone <repository_url>
   cd website/my_website

2. Create a virtual environment and activate it

   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate

3. Install dependencies

   pip install -r requirements.txt

4. Apply migrations

   python manage.py migrate

5. Run the development server

   python manage.py runserver

6. Access the site
Open your browser at http://127.0.0.1:8000/main

---

## Usage

- Navigate to /main for the index page.
- If unauthenticated, you will be redirected to /login.
- Register new users at /register, which logs in users immediately.
- Logout via /logout.

Note: Full session management and advanced user session features are planned for future development.

---

## Future Development

- Implement advanced session management (remember me, session expiration, etc.).
- Build interactive portfolio pages with dynamic content.
- Add frontend enhancements using modern styling or React components.
- Include analytics and project tracking for portfolio items.

---

## License

This project is open-source and available under the MIT License.
