# Personal Website Project

A Django-based personal portfolio platform focused on a passwordless ("magic link") authentication experience, plus a small collection of informational pages.

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

This repository powers a personal portfolio site built with Django. The `core` app owns public-facing pages, while the `accounts` app implements a passwordless login flow. Users register with an email address, receive verification links, and later sign in via one-time "magic" links.

---

## Features

- Passwordless auth: email-based verification and login links that expire after first use.
- Rate limiting: built-in throttling on login and registration email requests to prevent abuse.
- Async mail dispatch: magic-link emails send in the background so requests stay fast.
- Custom user model: `accounts.User` uses email as the identifier.
- Core marketing pages: static landing/about/projects pages under the `core` app.

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

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a `.env` file (or otherwise supply environment variables):

```
DJANGO_SECRET_KEY=change-me
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_DEBUG=True
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=app-specific-password
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the site at http://127.0.0.1:8000/core/ (core app) or http://127.0.0.1:8000/accounts/ (auth flows).

---

## Usage

- Register: POST `/accounts/register/` with an email/name to receive a verification link.
- Verify: click the emailed `/accounts/verify/?token=...` link to activate the account.
- Login: POST `/accounts/login/` to receive a single-use login link.
- Landing pages live under `/core/` and are safe for non-authenticated traffic.

Rate limits currently allow **3 registration attempts/hour** and **5 login-link requests/15 minutes** per email address.

---

## Future Development

- Improve user feedback and UI polish for auth flows.
- Expand portfolio content with dynamic project data.
- Integrate background task queue for email delivery if traffic grows.

---

## License

This project is open-source and available under the **MIT License**.