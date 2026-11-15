# INTERNSHIP PROJECT REPORT
## DIYInternship: Blogging Platform with Flask (Weeks 1 to 7)

**Candidate Name:** Shraddha Chavan  
**Project Title:** Full-Stack Modular Blogging Platform with Flask  
**Repository:** [https://github.com/chavanshraddha-blip/my-first-repo.git](https://github.com/chavanshraddha-blip/my-first-repo.git)  
**Date of Submission:** November 2026  
**Status:** All 7 Weeks Fully Implemented & Tested  

---

## 1. ABSTRACT

Modern web development demands maintainable, secure, and extensible system architectures. This project delivers a production-ready, full-stack blogging platform constructed using the Python Flask micro-framework and SQLAlchemy ORM. Spanning seven distinct development milestones outlined by DIYInternship, the platform encapsulates modular blueprint architecture, secure user authentication (Flask-Login, salted PBKDF2 hashing), rich text content publishing with Quill.js, relational categorization and tagging models, an interactive discussion and commenting engine, and dynamic multi-attribute search and filtering. The application features a responsive Bootstrap 5 interface, rigorous unit and integration test coverage via pytest, and deployment artifacts containerized using Docker and Gunicorn.

---

## 2. INTRODUCTION & PROJECT CONTEXT

Blogging platforms remain fundamental tools for digital knowledge sharing, technical documentation, and community building. Developing a custom blogging platform exposes developers to the complete lifecycle of software engineering: relational database schema modeling, modular routing, session security, cross-site scripting (XSS) defense, search query optimization, and test automation.

This project was built strictly according to the 7-week curriculum prescribed by DIYInternship. Each week targeted a specific architectural tier, culminating in a cohesive, deployable web application.

---

## 3. OBJECTIVES

The core objectives of this project are:
1. **Architectural Modularity**: Implement the Flask Application Factory Pattern and Blueprints to decouple application domains (`auth`, `main`, `posts`, `comments`).
2. **Identity & Session Security**: Deliver secure registration, login, logout, and password hashing with CSRF token verification.
3. **Content Lifecycle (CRUD)**: Enable full Create, Read, Update, and Delete operations for blog posts with category assignment, comma-separated tagging, and WYSIWYG rich text formatting.
4. **Intuitive User Interface**: Develop a clean, mobile-responsive frontend using Bootstrap 5 with pagination controls and author profiles.
5. **Interactive Engagement**: Facilitate community interaction through authenticated post commenting and authorized comment deletion.
6. **Information Discovery**: Provide full-text keyword search across titles and article bodies combined with category and tag filters.
7. **Quality Assurance & Deployment**: Implement comprehensive automated testing using pytest and prepare containerized production configurations using Docker and Gunicorn.

---

## 4. TOOLS & TECHNOLOGIES

| Category | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.11.9 | Core programming language |
| **Framework** | Flask | 3.1.3 | Web micro-framework |
| **Database & ORM** | SQLAlchemy / SQLite | 2.1.8 | Relational data persistence & object-relational mapping |
| **Migrations** | Flask-Migrate / Alembic | 4.1.0 / 1.20.1 | Database schema versioning |
| **Authentication** | Flask-Login | 0.6.3 | User session tracking and route protection |
| **Forms & Validation** | Flask-WTF / WTForms | 1.3.0 / 3.3.2 | Form rendering, CSRF protection, and data validation |
| **Sanitization** | Bleach | 6.4.0 | Server-side HTML sanitization for XSS mitigation |
| **Frontend Framework**| Bootstrap | 5.3.3 | Responsive CSS grid, components, and typography |
| **Icons & Fonts** | Bootstrap Icons & Google Fonts | 1.11.3 | Visual icons and Plus Jakarta Sans typography |
| **Rich Text Editor** | Quill.js | 2.0.2 | Client-side rich text formatting |
| **Testing** | pytest | 9.2.0 | Automated unit and integration test runner |
| **WSGI Server** | Gunicorn | 27.0.1 | Production WSGI HTTP server |
| **Containerization** | Docker | 24+ | Production container runtime and deployment |

---

## 5. SYSTEM ARCHITECTURE

The application adopts the **Application Factory Pattern** (`create_app`), ensuring independent application instances can be spawned for development, testing, and production environments.

### 5.1 Architecture Diagram

```
                +-----------------------------------------------+
                |            Client Browser / HTTP              |
                +-----------------------------------------------+
                                        |
                                        v
                +-----------------------------------------------+
                |           WSGI Server (Gunicorn)              |
                +-----------------------------------------------+
                                        |
                                        v
                +-----------------------------------------------+
                |        Flask Application Factory Pattern      |
                |               (app/__init__.py)               |
                +-----------------------------------------------+
                   |              |              |             |
                   v              v              v             v
             +----------+   +----------+   +----------+  +----------+
             | auth_bp  |   | main_bp  |   | posts_bp |  |comments_ |
             +----------+   +----------+   +----------+  +----------+
                   |              |              |             |
                   +--------------+--------------+-------------+
                                        |
                                        v
                +-----------------------------------------------+
                |         SQLAlchemy ORM Data Models            |
                |   User | Post | Category | Tag | Comment      |
                +-----------------------------------------------+
                                        |
                                        v
                +-----------------------------------------------+
                |        SQLite Database / PostgreSQL           |
                +-----------------------------------------------+
```

---

## 6. DATABASE DESIGN & SCHEMA

The database schema utilizes relational constraints, foreign keys, cascade deletes, and an association table for many-to-many relationships.

### 6.1 Entity-Relationship (ER) Overview

- **User**:
  - `id` (PK, Integer)
  - `username` (String 64, Unique, Indexed)
  - `email` (String 120, Unique, Indexed)
  - `password_hash` (String 256)
  - `bio` (Text)
  - `created_at` (DateTime)
  - *Relationships:* `posts` (1-to-Many), `comments` (1-to-Many)

- **Category**:
  - `id` (PK, Integer)
  - `name` (String 50, Unique)
  - `slug` (String 60, Unique, Indexed)
  - `description` (String 255)
  - *Relationship:* `posts` (1-to-Many)

- **Tag**:
  - `id` (PK, Integer)
  - `name` (String 50, Unique)
  - `slug` (String 60, Unique, Indexed)
  - *Relationship:* `posts` (Many-to-Many via `post_tags`)

- **post_tags** (Association Table):
  - `post_id` (FK to `posts.id`, PK, OnDelete CASCADE)
  - `tag_id` (FK to `tags.id`, PK, OnDelete CASCADE)

- **Post**:
  - `id` (PK, Integer)
  - `title` (String 150, Not Null)
  - `slug` (String 180, Indexed)
  - `content` (Text, Not Null)
  - `summary` (String 300)
  - `created_at` (DateTime, Indexed)
  - `updated_at` (DateTime)
  - `user_id` (FK to `users.id`, Not Null)
  - `category_id` (FK to `categories.id`, Nullable)
  - *Relationships:* `author` (User), `category` (Category), `tags` (List of Tag), `comments` (1-to-Many, Cascade All, Delete-Orphan)

- **Comment**:
  - `id` (PK, Integer)
  - `content` (Text, Not Null)
  - `created_at` (DateTime, Indexed)
  - `user_id` (FK to `users.id`, Not Null)
  - `post_id` (FK to `posts.id`, Not Null)
  - *Relationships:* `author` (User), `post` (Post)

---

## 7. WEEK-BY-WEEK IMPLEMENTATION DETAILS

### Week 1: Flask Setup & Basic Structure
- **Objective:** Establish the virtual environment, install packages, configure SQLAlchemy with SQLite, integrate Flask-Migrate, and set up the modular blueprint structure.
- **Files Created:**
  - `config.py` - Base, Development, Testing, Production configurations.
  - `app/__init__.py` - Factory function `create_app()`, error handlers, global context processors.
  - `app/extensions.py` - Shared instances of SQLAlchemy, Migrate, LoginManager.
  - `run.py` - Application launcher with CLI database initialization (`flask init-db`).
  - `requirements.txt` - Complete dependency specification.
  - `app/templates/base.html` - Master Jinja2 layout with navigation, flash banners, and footer.
  - `app/static/css/style.css` - Custom design styling.
  - `app/static/js/main.js` - Dynamic UI behaviors.
- **Outcome:** Clean running Flask application instance capable of modular expansion.

### Week 2: User Authentication & Session Management
- **Objective:** Implement user registration, login, logout, and session tracking using Flask-Login and Werkzeug password security.
- **Files Created:**
  - `app/models/user.py` - User model implementing `UserMixin`, `set_password()`, and `check_password()`.
  - `app/auth/forms.py` - `RegistrationForm` (with unique username/email validation), `LoginForm`, `EditProfileForm`.
  - `app/auth/routes.py` - Routes for `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/profile`.
  - `app/templates/auth/register.html` - Registration view with form feedback.
  - `app/templates/auth/login.html` - Login view with remember-me support.
  - `app/templates/auth/profile.html` - Profile edit and password update page.
- **Outcome:** Comprehensive, secure authentication system with flash notifications and protected routes (`@login_required`).

### Week 3: Blog Post CRUD Functionality & Rich Text
- **Objective:** Create models for Posts, Tags, and Categories. Build forms and routes for full CRUD operations with rich text editing and author authorization.
- **Files Created:**
  - `app/models/post.py` - Post model with reading time calculation and tag relationships.
  - `app/models/category.py` - Category model.
  - `app/models/tag.py` - Tag model.
  - `app/posts/forms.py` - `PostForm` with title, category select, tags, summary, and content.
  - `app/posts/routes.py` - Create, edit, and delete routes with 403 Forbidden enforcement on non-owners.
  - `app/utils.py` - URL slug generation and Bleach HTML sanitization.
  - `app/templates/posts/create_post.html` - Quill editor integrated post creator.
  - `app/templates/posts/edit_post.html` - Post editor with delete confirmation modal.
- **Outcome:** Robust publishing system allowing rich articles with automated slug creation and XSS prevention.

### Week 4: Frontend – Displaying Posts, Author Profiles & Pagination
- **Objective:** Build responsive Jinja2 templates for the homepage, article view, and author profile with pagination.
- **Files Created:**
  - `app/templates/main/index.html` - Homepage with hero section, post cards, categories, and tag cloud.
  - `app/templates/posts/post_detail.html` - Detailed article view with meta badges, reading time, and author bio.
  - `app/templates/main/user_profile.html` - Public author profile showcasing bio, stats, and published posts.
  - `app/templates/posts/my_posts.html` - Author dashboard listing all personal articles with quick actions.
- **Outcome:** A polished, mobile-friendly interface styled with Bootstrap 5 and accessible navigation.

### Week 5: Commenting System
- **Objective:** Allow authenticated readers to leave comments on blog posts with author and post-owner moderation abilities.
- **Files Created:**
  - `app/models/comment.py` - Comment model with timestamps and user/post foreign keys.
  - `app/comments/forms.py` - `CommentForm` with content length validation.
  - `app/comments/routes.py` - Add comment route and secure delete route.
  - Integrated into `app/templates/posts/post_detail.html` - Interactive discussion board with user avatars and delete controls.
- **Outcome:** Interactive community discussion platform with authorization checks protecting comment deletion.

### Week 6: Search and Multi-Criteria Filtering
- **Objective:** Enable keyword search across titles and content, combined with category and tag filtering, preserving query parameters during pagination.
- **Files Created:**
  - Updated `app/main/routes.py` - Implemented SQLAlchemy `or_` conditions and filter chaining for `q`, `category`, `tag`, and `sort`.
  - Updated `app/templates/main/index.html` - Added filter bar, active filter badges with remove buttons, and persistent pagination links.
- **Outcome:** High-performance search allowing complex compound queries (e.g. search keyword inside a specific category).

### Week 7: Deployment Preparation & Automated Testing
- **Objective:** Develop an automated pytest test suite and containerize the application for production using Docker and Gunicorn.
- **Files Created:**
  - `tests/conftest.py` - App fixtures, in-memory testing DB, test client, and authentication helpers.
  - `tests/test_auth.py` - 10 unit tests for authentication, sessions, and hashing.
  - `tests/test_posts.py` - 6 integration tests for CRUD and authorization boundaries.
  - `tests/test_comments.py` - 5 integration tests for commenting lifecycle and moderation.
  - `tests/test_search.py` - 6 integration tests for multi-filter querying.
  - `Dockerfile` - Multi-stage containerization with healthcheck and Gunicorn WSGI.
  - `.dockerignore` - Container build hygiene.
  - `DEPLOYMENT_GUIDE.md` - Step-by-step production deployment documentation.
- **Outcome:** Verified test suite covering all core application flows; production-ready container image.

---

## 8. RESULTS AND VERIFICATION

The application was executed locally and validated against all functional requirements:
1. **HTTP Status Code Verification**: All public routes return 200 OK; protected endpoints return 302 redirect to login when unauthenticated; unauthorized edits return 403 Forbidden.
2. **Database Integrity**: Cascade deletion confirmed; deleting a post deletes all associated comments and unlinks tags without deleting tags themselves.
3. **Responsive Testing**: Verified on desktop, tablet, and mobile viewport simulations.
4. **Automated Testing Suite**: 100% pass rate across all unit and integration test modules.

---

## 9. CONCLUSION

The Blogging Platform with Flask successfully meets all objectives specified for Weeks 1 through 7 of the DIYInternship curriculum. By prioritizing modular architecture, secure user flows, robust data modeling, and responsive frontend design, the project serves as an exemplary full-stack web application ready for production deployment.
