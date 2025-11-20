# Personal Website Project

A Django-based personal website project aimed at showcasing backend development skills while building the foundation for a professional portfolio platform. The project currently focuses on backend functionality, with a basic frontend skeleton to support future interactive features.

---

## Table of Contents

- [Overview](#overview)  
- [Technology Stack](#technology-stack)  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Future Development](#future-development)  
- [License](#license)  

---

## Overview

This Django project is a personal website designed to demonstrate backend engineering capabilities, while serving as a platform for a portfolio.  

Current backend functionality includes:

- Passwordless user registration and login using **magic links** sent via email  
- Email verification workflow to ensure valid accounts  
- Mailing list opt-in system for newsletters and updates  
- Custom User model storing extended information (email, name, verification status, consent)  
- Basic frontend skeleton using HTML and Tailwind CSS for structure and forms  

The project is intended to evolve into a fully interactive portfolio website with dynamic content and modern frontend enhancements.

---

## Technology Stack

- Python 3.11  
- Django 5.x  
- SQLite (default; can be swapped with PostgreSQL or other DB)  
- Tailwind CSS (frontend skeleton)  

---

## Features

- **User Authentication**: Register and log in using secure, signed email tokens (magic links)  
- **Email Verification**: Users must verify their email before gaining full access  
- **Mailing List Consent**: Optional opt-in during registration for newsletters  
- **Custom User Model**: Stores email, name, verification status, and mailing list preference  
- **Backend-Focused Architecture**: Demonstrates session management, token signing, and secure flows  
- **Basic HTML Templates**: Provide structural placeholders for future interactive pages  

---

## Installation

1. Clone the repository:

```
git clone https://github.com/OhACD/website
cd website/my_website
```

2. Create a virtual environment and activate it:

```
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / Mac
source .venv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Apply migrations:

```
python manage.py migrate
```

5. Run the development server:

```
python manage.py runserver
```

6. Access the site at: [http://127.0.0.1:8000/core](http://127.0.0.1:8000/core)

---

## Usage

- Visit `/core` for the landing page with links to registration, login, and site sections.  
- Registration allows users to opt-in to the mailing list.  
- Users receive a verification email; clicking the link completes registration.  
- Login uses a **magic link** sent to the registered email—no password required.  
- Templates currently provide basic structure and forms; frontend enhancements will be added in future updates.  
- Email testing can be done via Django console backend or a configured SMTP server.

---

## Future Development

- Expand frontend with **Tailwind CSS or React** for interactive, polished UI  
- Implement **comment and like system** for portfolio projects  
- Add **user dashboards and profiles** for logged-in users  
- Enhance session management (session expiration, "remember me")  
- Integrate analytics for project interactions and views  
- Implement real mailing list integration (Mailchimp, SendGrid, etc.)  
- Add additional backend features for a fully dynamic portfolio experience  

---

## License

This project is open-source and available under the **MIT License**.