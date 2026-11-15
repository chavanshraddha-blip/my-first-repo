# DIY INTERNSHIP – WEEKLY TASKS DOCUMENTATION
## Blogging Platform with Flask (Weeks 1 to 7)

**Intern Name:** Shraddha Chavan  
**Project:** Blogging Platform with Flask  
**GitHub Repository:** [https://github.com/chavanshraddha-blip/my-first-repo.git](https://github.com/chavanshraddha-blip/my-first-repo.git)  

---

## WEEK 1: FLASK SETUP AND BASIC STRUCTURE

### 1. Objective
Set up the Python Flask environment, configure a modular architecture using the Application Factory Pattern and Flask Blueprints, configure the SQLite database with SQLAlchemy ORM, integrate Flask-Migrate, and construct base Jinja2 templates and static asset folders.

### 2. Implementation
- Created a Python virtual environment (`venv`) using Python 3.11.
- Initialized Git version control with a `main` branch and created `.gitignore` and `.env.example`.
- Configured environment classes in `config.py` for Development, Testing, and Production.
- Implemented `create_app()` factory in `app/__init__.py` with Blueprint registration:
  - `main_bp` (`/`)
  - `auth_bp` (`/auth`)
  - `posts_bp` (`/posts`)
  - `comments_bp` (`/comments`)
- Integrated `SQLAlchemy` and `Flask-Migrate` in `app/extensions.py`.
- Developed `base.html` master template with responsive navbar, flash message alerts, and footer.
- Added custom CSS (`app/static/css/style.css`) and JavaScript (`app/static/js/main.js`).
- Created `run.py` launcher with a custom CLI command `flask init-db` for seeding.

### 3. Files Created / Modified
- `config.py`
- `requirements.txt`
- `.gitignore`
- `.env.example`
- `run.py`
- `app/__init__.py`
- `app/extensions.py`
- `app/templates/base.html`
- `app/static/css/style.css`
- `app/static/js/main.js`

### 4. Features Completed
- ✅ Virtual environment established.
- ✅ Modular Flask Blueprints registered.
- ✅ SQLAlchemy and SQLite database configuration.
- ✅ Jinja2 template inheritance structure.
- ✅ Application configuration management.

### 5. Testing Evidence
- Flask application instantiated successfully via `create_app()`.
- Routes return HTTP 200 responses.
- Static CSS and JS assets load correctly with Bootstrap 5.

### 6. Remaining Issues
- None. All Week 1 requirements completed.

---

## WEEK 2: USER AUTHENTICATION

### 1. Objective
Implement user registration, login, logout, and session management using Flask-Login and Werkzeug password hashing.

### 2. Implementation
- Created the `User` model inheriting from `UserMixin` in `app/models/user.py`.
- Implemented secure password hashing via `generate_password_hash()` and `check_password_hash()`.
- Built `RegistrationForm`, `LoginForm`, and `EditProfileForm` in `app/auth/forms.py` with custom validators for uniqueness.
- Configured Flask-Login `login_manager` with login view, warning message category, and user loader.
- Implemented session management in `app/auth/routes.py` with safe `next` parameter redirect handling to prevent open-redirect vulnerabilities.
- Added user profile edit functionality allowing bio updates and optional password changes.

### 3. Files Created / Modified
- `app/models/user.py`
- `app/auth/forms.py`
- `app/auth/routes.py`
- `app/templates/auth/register.html`
- `app/templates/auth/login.html`
- `app/templates/auth/profile.html`

### 4. Features Completed
- ✅ User registration with unique username and email validation.
- ✅ Salted password hashing (no plain passwords in database).
- ✅ Login with either username or email and remember-me checkbox.
- ✅ Safe logout and session termination.
- ✅ Flash messages for successful and failed authentication attempts.
- ✅ Protected routes guarded by `@login_required`.

### 5. Testing Evidence
- Unit tests in `tests/test_auth.py` covering registration, duplicate errors, valid login, invalid credentials, logout, and unauthorized access redirects (100% pass).

### 6. Remaining Issues
- None. All Week 2 requirements completed.

---

## WEEK 3: BLOG POST CRUD FUNCTIONALITY

### 1. Objective
Create models for Posts, Tags, and Categories. Implement routes and forms (Flask-WTF) for creating, reading, updating, and deleting blog posts with Quill rich text editor and ownership verification.

### 2. Implementation
- Created `Post`, `Category`, `Tag`, and `post_tags` models in `app/models/`.
- Established relational integrity:
  - User -> Posts (one-to-many)
  - Category -> Posts (one-to-many)
  - Post <-> Tags (many-to-many via `post_tags` with cascade delete)
- Integrated Quill 2.0.2 rich text editor on frontend, paired with hidden textarea synchronization in `main.js`.
- Implemented server-side HTML sanitization in `app/utils.py` using `bleach` to block XSS payloads.
- Added post ownership validation in edit and delete routes: non-authors receive HTTP 403 Forbidden.
- Added estimated reading time computation property (`post.reading_time`).

### 3. Files Created / Modified
- `app/models/post.py`
- `app/models/category.py`
- `app/models/tag.py`
- `app/posts/forms.py`
- `app/posts/routes.py`
- `app/utils.py`
- `app/templates/posts/create_post.html`
- `app/templates/posts/edit_post.html`

### 4. Features Completed
- ✅ Create, read, update, and delete blog posts.
- ✅ Category selection dropdown and comma-separated tag assignment.
- ✅ WYSIWYG rich text formatting with Quill.
- ✅ Server-side XSS sanitization using Bleach.
- ✅ Strict author ownership verification before edits or deletes (HTTP 403).
- ✅ CSRF protection on all forms.

### 5. Testing Evidence
- Integration tests in `tests/test_posts.py` verifying post creation, reading, authorized editing, unauthorized edit rejection, and cascade deletion (100% pass).

### 6. Remaining Issues
- None. All Week 3 requirements completed.

---

## WEEK 4: FRONTEND – DISPLAYING POSTS AND NAVIGATION

### 1. Objective
Develop responsive Jinja2 templates for the homepage (listing posts), individual post view, and user profile pages with pagination.

### 2. Implementation
- Designed the homepage (`app/templates/main/index.html`) featuring a Hero banner, post cards with reading time, category badges, author avatars, and right-hand sidebar.
- Created `post_detail.html` with breadcrumbs, author profile block, rich text post body, tags, and related category articles.
- Implemented `user_profile.html` displaying public user statistics (total articles, total comments) and paginated list of user's posts.
- Added `my_posts.html` dashboard allowing authors to view, edit, or delete their articles from a table view.
- Implemented responsive Bootstrap 5 pagination controls supporting previous, numbered, and next navigation.

### 3. Files Created / Modified
- `app/templates/main/index.html`
- `app/templates/posts/post_detail.html`
- `app/templates/main/user_profile.html`
- `app/templates/posts/my_posts.html`
- `app/templates/posts/category_posts.html`
- `app/templates/posts/tag_posts.html`
- `app/templates/main/about.html`

### 4. Features Completed
- ✅ Template inheritance with `base.html`.
- ✅ Professional responsive homepage with blog cards.
- ✅ Detailed single article page with author bio and related articles.
- ✅ Public user profile page with author's posts and statistics.
- ✅ Author's personal articles dashboard.
- ✅ Reusable Bootstrap 5 pagination component.

### 5. Testing Evidence
- Verified pages render with HTTP 200 on mobile, tablet, and desktop viewports.
- Tested pagination with multiple pages of records.

### 6. Remaining Issues
- None. All Week 4 requirements completed.

---

## WEEK 5: COMMENTING SYSTEM

### 1. Objective
Allow authenticated users to comment on posts. Implement models, forms, and views for adding and removing comments with authorization checks.

### 2. Implementation
- Created `Comment` model in `app/models/comment.py` with foreign keys to `users.id` and `posts.id`.
- Established `Post.comments` relationship with `cascade="all, delete-orphan"` so deleting a post deletes its comments.
- Built `CommentForm` in `app/comments/forms.py` with validation.
- Implemented `add_comment` route in `app/comments/routes.py` with `@login_required`.
- Implemented `delete_comment` route verifying that either the comment author or the post author can delete the comment (403 for unauthorized users).
- Integrated comments section in `post_detail.html` with author badges, timestamp, and delete controls.

### 3. Files Created / Modified
- `app/models/comment.py`
- `app/comments/forms.py`
- `app/comments/routes.py`
- `app/templates/posts/post_detail.html`

### 4. Features Completed
- ✅ Comment database model with relationships to Post and User.
- ✅ Authenticated comment submission form.
- ✅ Display comments chronologically below the blog post.
- ✅ Authorization to delete comments by comment author or post owner.
- ✅ Guest prompt to log in before commenting.

### 5. Testing Evidence
- Tests in `tests/test_comments.py` covering comment creation, unauthenticated redirects, authorized deletion, unauthorized deletion blocking, and post author moderation (100% pass).

### 6. Remaining Issues
- None. All Week 5 requirements completed.

---

## WEEK 6: SEARCH AND FILTERING

### 1. Objective
Add functionality to search for posts by title or content, and filter by tags and categories, preserving query parameters during pagination.

### 2. Implementation
- Updated `index()` route in `app/main/routes.py` with SQLAlchemy `or_` query:
  ```python
  query = query.filter(
      or_(
          Post.title.ilike(f"%{q}%"),
          Post.content.ilike(f"%{q}%"),
          Post.summary.ilike(f"%{q}%")
      )
  )
  ```
- Implemented category filtering by slug (`Post.category_id == active_category.id`).
- Implemented tag filtering by slug (`Post.tags.contains(active_tag)`).
- Added sorting options: newest first vs. oldest first.
- Updated pagination links in `index.html` to append `q`, `category`, `tag`, and `sort` query parameters to prevent filter reset upon navigating pages.
- Built interactive filter bar with active filter badges and one-click removal.

### 3. Files Created / Modified
- `app/main/routes.py`
- `app/templates/main/index.html`

### 4. Features Completed
- ✅ Search bar with live keyword filtering over title and content.
- ✅ Category dropdown filtering with post counts.
- ✅ Tag cloud filtering by clicking tag badges.
- ✅ Multi-criteria filtering (combining keyword search with category/tag).
- ✅ Sort ordering by newest and oldest.
- ✅ Preserved query parameters across pagination.
- ✅ Friendly empty-state UI when no results match.

### 5. Testing Evidence
- Automated test suite in `tests/test_search.py` validating title search, content search, category filtering, tag filtering, combined querying, and empty results (100% pass).

### 6. Remaining Issues
- None. All Week 6 requirements completed.

---

## WEEK 7: DEPLOYMENT PREPARATION AND TESTING

### 1. Objective
Write comprehensive unit tests for core functionalities. Prepare the application for production deployment using Gunicorn and Docker.

### 2. Implementation
- Configured `pytest` with fixtures in `tests/conftest.py` utilizing in-memory SQLite and disabled CSRF for headless client testing.
- Wrote 27 test cases across 4 test modules:
  - `tests/test_auth.py`
  - `tests/test_posts.py`
  - `tests/test_comments.py`
  - `tests/test_search.py`
- Created `Dockerfile` with multi-stage / slim Python 3.11 base, dependency caching, healthcheck probe, and Gunicorn entrypoint.
- Created `.dockerignore` to keep image footprint small and secure.
- Added `DEPLOYMENT_GUIDE.md` detailing local, VPS, and Docker deployment workflows.

### 3. Files Created / Modified
- `tests/conftest.py`
- `tests/test_auth.py`
- `tests/test_posts.py`
- `tests/test_comments.py`
- `tests/test_search.py`
- `Dockerfile`
- `.dockerignore`
- `DEPLOYMENT_GUIDE.md`
- `TESTING_REPORT.md`

### 4. Features Completed
- ✅ Automated pytest test suite covering all functional modules.
- ✅ Gunicorn WSGI production server configuration.
- ✅ Docker containerization with healthcheck probe.
- ✅ Environment variable configuration via `.env`.
- ✅ Complete deployment and testing documentation.

### 5. Testing Evidence
- Test suite executed with pytest; all tests passed.
- Gunicorn configuration verified.

### 6. Remaining Issues
- None. All Week 7 requirements completed.
