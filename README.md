# DevLog - Modern Blogging Platform with Flask

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg)](https://palletsprojects.com/p/flask/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red.svg)](https://www.sqlalchemy.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A complete, responsive, full-featured web blogging platform built from scratch with Python, Flask, SQLAlchemy, Flask-Login, and Bootstrap 5. Developed according to the exact weekly specifications of the **DIYInternship** curriculum (Weeks 1 to 7).

---

## 📑 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Weekly Milestones Summary](#weekly-milestones-summary)
- [Technology Stack](#technology-stack)
- [Project Directory Structure](#project-directory-structure)
- [Installation & Local Setup](#installation--local-setup)
- [Database Migrations & Seeding](#database-migrations--seeding)
- [Running Automated Tests](#running-automated-tests)
- [Containerization & Docker Deployment](#containerization--docker-deployment)
- [Security & Best Practices](#security--best-practices)
- [Contributing & License](#contributing--license)

---

## 🌟 Overview

**DevLog** is a modular web application that allows software developers, students, and technology writers to publish technical tutorials, engage in discussions via comments, organize content using tags and categories, and search articles seamlessly. The platform provides a modern user interface powered by Bootstrap 5 and the Quill rich text editor, backed by a robust Flask architecture utilizing the Application Factory Pattern and Blueprints.

---

## 🚀 Key Features

- **Modular Blueprints Architecture**: Strict separation of concerns with `auth`, `main`, `posts`, and `comments` modules.
- **Secure Authentication**: User registration, login with session persistence, profile management, and password hashing with Werkzeug.
- **Rich Text Article Publishing**: Quill WYSIWYG editor integration with server-side HTML sanitization (Bleach) to prevent XSS.
- **Relational Data Modeling**: Many-to-many relationship between Posts and Tags; one-to-many relationships for Categories, Authors, and Comments.
- **Dynamic Commenting System**: Authenticated users can leave comments; authors and commenters can manage their contributions.
- **Comprehensive Search & Filtering**: Multi-condition querying by keyword (title and body), category, and tags, with filter preservation across pagination.
- **Modern Responsive Frontend**: Built with Bootstrap 5, featuring cards, modals, badges, interactive dropdowns, and mobile-friendly navigation.
- **Automated Testing Suite**: Full pytest test suite covering authentication, route authorization, CRUD operations, comments, and search.
- **Production-Ready Deployment**: Configured with Gunicorn WSGI server and Docker containerization.

---

## 📅 Weekly Milestones Summary

| Week | Phase / Focus | Key Deliverables | Status |
| :---: | :--- | :--- | :---: |
| **Week 1** | **Flask Setup & Architecture** | Application factory, Blueprints, SQLAlchemy ORM, Flask-Migrate, base layout | ✅ Completed |
| **Week 2** | **User Authentication** | User model, Flask-Login, password hashing, registration, login/logout, profile | ✅ Completed |
| **Week 3** | **Blog Post CRUD Functionality** | Post, Tag, Category models, Flask-WTF forms, Quill rich editor, ownership verification | ✅ Completed |
| **Week 4** | **Frontend & Navigation** | Jinja2 templates, article detail view, public author profiles, pagination controls | ✅ Completed |
| **Week 5** | **Commenting System** | Comment model, relationships, post comments, deletion authorization, avatar display | ✅ Completed |
| **Week 6** | **Search & Filtering** | Search bar (title & content), category & tag filters, pagination parameter preservation | ✅ Completed |
| **Week 7** | **Testing & Deployment** | Pytest test suite, Gunicorn WSGI configuration, Dockerfile, production settings | ✅ Completed |

---

## 🛠 Technology Stack

- **Backend Framework**: [Flask 3.x](https://flask.palletsprojects.com/)
- **Database & ORM**: [SQLAlchemy 2.x](https://www.sqlalchemy.org/) with [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) & SQLite (PostgreSQL compatible)
- **Migrations**: [Flask-Migrate](https://flask-migrate.readthedocs.io/) & [Alembic](https://alembic.sqlalchemy.org/)
- **Authentication**: [Flask-Login](https://flask-login.readthedocs.io/) & [Werkzeug Security](https://werkzeug.palletsprojects.com/)
- **Forms & Validation**: [Flask-WTF](https://flask-wtf.readthedocs.io/) & [WTForms](https://wtforms.readthedocs.io/) & [email-validator](https://github.com/JoshData/python-email-validator)
- **HTML Sanitization**: [Bleach](https://github.com/mozilla/bleach)
- **Frontend / Styling**: [Bootstrap 5.3](https://getbootstrap.com/), [Bootstrap Icons](https://icons.getbootstrap.com/), Google Fonts (*Plus Jakarta Sans* & *JetBrains Mono*)
- **Rich Text Editor**: [Quill.js 2.x](https://quilljs.com/)
- **Testing**: [pytest 8.x](https://pytest.org/)
- **WSGI / Deployment**: [Gunicorn](https://gunicorn.org/) & [Docker](https://www.docker.com/)

---

## 📂 Project Directory Structure

```text
Blogging-Platform-Flask/
│
├── app/
│   ├── __init__.py          # Flask Application Factory & Error Handlers
│   ├── extensions.py        # Extensions initialization (db, migrate, login_manager)
│   ├── utils.py             # Slug generator, HTML sanitizer (Bleach)
│   ├── auth/                # Authentication Blueprint
│   │   ├── __init__.py
│   │   ├── forms.py         # RegistrationForm, LoginForm, EditProfileForm
│   │   └── routes.py        # Login, Register, Logout, Profile routes
│   ├── main/                # Main Blueprint
│   │   ├── __init__.py
│   │   └── routes.py        # Index (search/filter/pagination), User Profile, About
│   ├── posts/               # Posts CRUD Blueprint
│   │   ├── __init__.py
│   │   ├── forms.py         # PostForm (WTForms)
│   │   └── routes.py        # Create, Read, Update, Delete, Category, Tag routes
│   ├── comments/            # Comments Blueprint
│   │   ├── __init__.py
│   │   ├── forms.py         # CommentForm
│   │   └── routes.py        # Add comment, Delete comment
│   ├── models/              # SQLAlchemy Database Models
│   │   ├── __init__.py
│   │   ├── user.py          # User model & Flask-Login user_loader
│   │   ├── post.py          # Post model & post_tags association table
│   │   ├── category.py      # Category model
│   │   ├── tag.py           # Tag model
│   │   └── comment.py       # Comment model
│   ├── templates/           # Jinja2 HTML Templates
│   │   ├── base.html        # Master layout (Navbar, Flash alerts, Footer)
│   │   ├── auth/            # login.html, register.html, profile.html
│   │   ├── main/            # index.html, user_profile.html, about.html
│   │   ├── posts/           # post_detail.html, create_post.html, edit_post.html, ...
│   │   └── errors/          # 403.html, 404.html, 500.html
│   └── static/              # Static Assets
│       ├── css/
│       │   └── style.css    # Custom CSS & component overrides
│       └── js/
│           └── main.js      # Quill editor sync, auto-dismiss alerts, modals
│
├── instance/                # SQLite database folder (auto-generated)
├── migrations/              # Database migration scripts (Alembic)
├── tests/                   # Pytest Automated Test Suite
│   ├── __init__.py
│   ├── conftest.py          # App fixtures, test client, mock data
│   ├── test_auth.py         # Authentication tests
│   ├── test_posts.py        # Post CRUD & authorization tests
│   ├── test_comments.py     # Comment functionality tests
│   └── test_search.py       # Search & multi-filter tests
│
├── config.py                # Environment configuration classes
├── run.py                   # Application entrypoint & CLI commands
├── requirements.txt         # Project Python dependencies
├── Dockerfile               # Container build configuration
├── .dockerignore            # Files excluded from Docker image
├── .gitignore               # Files excluded from Git version control
├── .env.example             # Example environment variables
├── README.md                # Project documentation
├── PROJECT_REPORT.md        # Academic internship comprehensive report
├── WEEKLY_TASKS.md          # Week-by-week implementation breakdown
├── TESTING_REPORT.md        # Detailed test cases and results
└── DEPLOYMENT_GUIDE.md      # Production deployment walkthrough
```

---

## ⚡ Installation & Local Setup

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.11)
- Git 2.x
- Virtualenv (`pip install virtualenv` or builtin `venv`)

### 2. Clone the Repository
```bash
git clone https://github.com/chavanshraddha-blip/my-first-repo.git
cd Blogging-Platform-Flask
```

### 3. Create and Activate Virtual Environment
```bash
# Windows (PowerShell / Command Prompt)
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

---

## 🗄 Database Migrations & Seeding

Initialize the SQLite database and seed initial categories and tags:
```bash
flask init-db
```
Or start the application directly with `python run.py`, which creates tables automatically on first startup:
```bash
python run.py
```
Visit the running application at: `http://127.0.0.1:5000`

---

## 🧪 Running Automated Tests

Run the comprehensive pytest suite:
```bash
# Run all tests
pytest -v

# Run with output and test summaries
pytest -v --tb=short
```

---

## 🐳 Containerization & Docker Deployment

### 1. Build Docker Image
```bash
docker build -t devlog-flask-app .
```

### 2. Run Docker Container
```bash
docker run -d -p 5000:5000 --name devlog-app devlog-flask-app
```
Access the application in your browser at `http://localhost:5000`.

---

## 🔒 Security Best Practices

- **CSRF Protection**: Form submissions validated with Flask-WTF CSRF tokens.
- **XSS Prevention**: User-submitted Quill rich text sanitized using Mozilla `bleach`.
- **Password Protection**: Hashed using salted PBKDF2/SHA-256 via `werkzeug.security`.
- **Ownership Verification**: Route decorators and checks verify user authorization before modifying or deleting resources (HTTP 403 response on violation).
- **SQL Injection Prevention**: Safe parameterization via SQLAlchemy ORM queries.

---

## 📜 License & Acknowledgments

This project is submitted for the **DIYInternship** program.
Developed by Shraddha Chavan. Licensed under the MIT License.
