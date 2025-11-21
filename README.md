# Personal Website Project

A Django-based personal portfolio platform focused on a passwordless ("magic link") authentication experience, plus a collection of informational pages. Built with modern UX principles, clean animations, and comprehensive documentation.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Security](#security)
- [Future Development](#future-development)
- [License](#license)

---

## Overview

This repository powers a personal portfolio site built with Django. The `core` app owns public-facing pages (landing, about, projects), while the `accounts` app implements a passwordless login flow. Users register with an email address, receive verification links, and later sign in via one-time "magic" links that expire after use.

The project emphasizes:
- **Clean UX**: Smooth animations, loading states, and keyboard navigation
- **Accessibility**: ARIA labels, focus states, and semantic HTML
- **Security**: Rate limiting, token expiration, and secure token signing
- **Code Quality**: Comprehensive documentation, type hints, and error handling

---

## Features

### Authentication
- **Passwordless auth**: Email-based verification and login links that expire after first use
- **Rate limiting**: Built-in throttling on login (5 requests/15 min) and registration (3 requests/hour) to prevent abuse
- **Async mail dispatch**: Magic-link emails send in the background so requests stay fast
- **Custom user model**: `accounts.User` uses email as the primary identifier
- **Token security**: Signed tokens with expiration and one-time use enforcement

### Frontend
- **Modern UI**: Dark theme with pastel accents and glassmorphism effects
- **Smooth animations**: Fade-in effects, hover transitions, and loading states
- **Responsive design**: Mobile-first approach with Tailwind CSS
- **Accessibility**: ARIA labels, keyboard navigation, and focus indicators
- **Form validation**: Client-side and server-side validation with clear error messages

### Code Quality
- **Comprehensive documentation**: Docstrings for all functions and classes
- **Type hints**: Type annotations for better code clarity
- **Error handling**: Graceful error handling with user-friendly messages
- **Code organization**: Clear separation of concerns across apps

---

## Technology Stack

- **Backend**: Django 5.2.3
- **Frontend**: Tailwind CSS 3.4.13
- **Database**: SQLite (development)
- **Email**: SMTP (Gmail)
- **Environment**: python-dotenv

---

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+ (for Tailwind CSS)
- npm or yarn

### Steps

1. **Clone the repository:**

```bash
git clone https://github.com/OhACD/website
cd website
```

2. **Create a virtual environment and activate it:**

```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. **Install Python dependencies:**

```bash
cd my_website
pip install -r ../requirements.txt
```

4. **Install Node dependencies:**

```bash
cd ..
npm install
```

5. **Build Tailwind CSS:**

```bash
npm run tw:build
```

Or for development with watch mode:

```bash
npm run tw:watch
```

6. **Apply migrations:**

```bash
cd my_website
python manage.py migrate
```

7. **Create a superuser (optional):**

```bash
python manage.py createsuperuser
```

---

## Configuration

Create a `.env` file in the project root (or set environment variables):

```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_DEBUG=True
DJANGO_CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

# Email Configuration (Gmail)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

### Gmail Setup

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an app-specific password
3. Use that password in `EMAIL_HOST_PASSWORD`

---

## Usage

### Running the Development Server

```bash
cd my_website
python manage.py runserver
```

Access the site at:
- Landing page: http://127.0.0.1:8000/core/
- Admin panel: http://127.0.0.1:8000/admin/
- Accounts: http://127.0.0.1:8000/accounts/

### User Flow

1. **Register**: Visit `/accounts/register/` and provide email/name
   - Receive verification email
   - Click verification link to activate account

2. **Login**: Visit `/accounts/login/` and provide email
   - Receive magic link email
   - Click link to authenticate (one-time use)

3. **Browse**: Public pages at `/core/` are accessible without authentication

### Rate Limits

- **Registration**: 3 attempts per hour per email
- **Login**: 5 requests per 15 minutes per email

---

## Project Structure

```
website/
├── my_website/              # Django project root
│   ├── accounts/            # Authentication app
│   │   ├── models.py       # User and MagicLink models
│   │   ├── views.py        # Registration, login, verification views
│   │   ├── services.py     # Email sending functions
│   │   ├── tokens.py       # Token generation/verification
│   │   ├── rate_limit.py   # Rate limiting logic
│   │   └── templates/      # Auth templates
│   ├── core/               # Public pages app
│   │   ├── views.py        # Landing, about, projects views
│   │   └── templates/      # Public page templates
│   ├── main/               # Legacy app (may be removed)
│   └── my_website/         # Project settings
│       ├── settings.py     # Django configuration
│       └── urls.py         # URL routing
├── assets/                 # Source CSS files
│   └── css/
│       └── input.css       # Tailwind input
├── static/                 # Compiled static files
│   └── css/
│       └── output.css      # Tailwind output
├── requirements.txt        # Python dependencies
├── package.json           # Node dependencies
├── tailwind.config.js     # Tailwind configuration
└── README.md              # This file
```

---

## Development

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Adding Features

1. **New Pages**: Add views in `core/views.py` and templates in `core/templates/`
2. **Auth Changes**: Modify `accounts/` app files
3. **Styling**: Update Tailwind classes or add custom CSS in `layout.html`

### Testing

Run Django tests:

```bash
cd my_website
python manage.py test
```

### Building for Production

1. Set `DJANGO_DEBUG=False` in environment
2. Update `ALLOWED_HOSTS` with production domain
3. Use a production database (PostgreSQL recommended)
4. Configure proper email backend
5. Set up static file serving (WhiteNoise or CDN)
6. Build Tailwind CSS: `npm run tw:build`

---

## Security

### Implemented Security Features

- **CSRF Protection**: Enabled via Django middleware
- **Rate Limiting**: Prevents abuse of email endpoints
- **Token Security**: Signed tokens with expiration
- **One-Time Tokens**: Magic links expire after use
- **Input Validation**: Email and name validation
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Django templates auto-escape

### Security Best Practices

- Never commit `.env` files
- Use strong `SECRET_KEY` in production
- Enable HTTPS in production
- Regularly update dependencies
- Monitor rate limit violations

---

## Future Development

### Planned Features

- [ ] HTML email templates for better email UX
- [ ] Background task queue (Celery) for email delivery
- [ ] Dynamic project data from GitHub API
- [ ] User profile pages
- [ ] Blog/content management system
- [ ] Analytics integration
- [ ] Dark/light theme toggle
- [ ] Internationalization (i18n)

### Improvements

- [ ] Add unit tests for all views
- [ ] Add integration tests for auth flow
- [ ] Performance optimization (caching, database queries)
- [ ] Add API endpoints
- [ ] Docker containerization
- [ ] CI/CD pipeline improvements

---

## License

This project is open-source and available under the MIT License.

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

---

## Contact

- **Email**: imadeldeen007@gmail.com
- **GitHub**: [OhACD](https://github.com/OhACD)

---

## Acknowledgments

Built with Django, Tailwind CSS, and a focus on clean, maintainable code.
