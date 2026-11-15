# AUTOMATED TESTING REPORT
## DevLog Blogging Platform (Week 7 Quality Assurance)

**Project:** Blogging Platform with Flask  
**Testing Framework:** pytest 9.x / Python unittest & Flask Test Client  
**Execution Environment:** In-Memory SQLite (`sqlite:///:memory:`)  
**CSRF Protection in Tests:** Disabled (`WTF_CSRF_ENABLED = False`) for headless API requests  

---

## 1. Executive Summary

This report documents the automated test suite developed for the Blogging Platform according to the Week 7 specifications of DIYInternship. The test suite verifies critical business logic, data models, relational constraints, route authorization, session handling, XSS protection, and multi-criteria search queries.

- **Total Test Cases:** 27
- **Test Modules:** 4
- **Passed:** 27
- **Failed:** 0
- **Code Coverage Target:** Core business logic, auth routes, CRUD operations, comments, and search.

---

## 2. Test Suite Architecture

The test suite is structured under `tests/`:
```text
tests/
├── __init__.py
├── conftest.py          # Application fixtures, database teardown, mock sessions
├── test_auth.py         # 10 test cases: user auth, password hashing, sessions
├── test_posts.py        # 6 test cases: CRUD operations & ownership authorization
├── test_comments.py     # 5 test cases: comment lifecycle & moderation
└── test_search.py       # 6 test cases: title/content search & combined filters
```

### Pytest Fixture Strategy (`tests/conftest.py`)
1. **`app` fixture:** Uses `create_app('testing')` to instantiate the application with an in-memory SQLite database and test secrets. Runs `db.create_all()` and seeds default categories and tags before yielding the application, then tears down with `db.drop_all()`.
2. **`client` fixture:** Returns the Flask test client (`app.test_client()`).
3. **`auth` fixture:** Encapsulates common user workflows (`register`, `login`, `logout`) to eliminate boilerplate in individual tests.
4. **`sample_user` & `sample_post` fixtures:** Provide pre-seeded fixtures for relational testing.

---

## 3. Test Cases & Results Breakdown

### Module 1: User Authentication (`tests/test_auth.py`)

| Test Case | Description | Expected Result | Status |
| :--- | :--- | :--- | :---: |
| `test_user_password_hashing` | Verifies Werkzeug salted hash generation and verification. | Password hash is not plain text; check_password returns True for match and False for mismatch. | **PASS** |
| `test_registration_success` | Tests valid user account creation. | Returns 200, flashes success, user persisted in DB with lowercase email. | **PASS** |
| `test_registration_duplicate_username` | Tests registration with an existing username. | Form rejected with "This username is already taken." | **PASS** |
| `test_registration_duplicate_email` | Tests registration with an existing email. | Form rejected with "An account with this email already exists." | **PASS** |
| `test_registration_password_mismatch` | Tests password confirmation inequality. | Form rejected with "Passwords must match." | **PASS** |
| `test_login_with_username_success` | Tests login using valid username and password. | Session established; flash "Welcome back, {username}!". | **PASS** |
| `test_login_with_email_success` | Tests login using valid email and password. | Session established; flash "Welcome back, {username}!". | **PASS** |
| `test_login_invalid_password` | Tests login attempt with wrong password. | Session not established; error flash displayed. | **PASS** |
| `test_logout` | Tests user session invalidation on logout. | User session cleared; redirects to home with info flash. | **PASS** |
| `test_login_required_protection` | Tests accessing `/posts/create` without authentication. | Redirects (302) to login page with `next` query parameter. | **PASS** |

---

### Module 2: Blog Post CRUD Operations (`tests/test_posts.py`)

| Test Case | Description | Expected Result | Status |
| :--- | :--- | :--- | :---: |
| `test_create_post` | Tests creating a post with categories and comma-separated tags. | Post created; tags parsed and linked; returns 200 with success flash. | **PASS** |
| `test_post_detail_view` | Tests fetching the detail page of an existing post. | Returns 200; title and content rendered. | **PASS** |
| `test_edit_post_by_author` | Tests modifying a post by the original creator. | Post updated in database; title and content match new values. | **PASS** |
| `test_edit_post_unauthorized` | Tests editing a post by a user who is not the author. | Aborts with HTTP 403 Forbidden. Post unchanged. | **PASS** |
| `test_delete_post_by_author` | Tests deleting a post by the author. | Post removed from database; returns redirect to index. | **PASS** |
| `test_delete_post_unauthorized` | Tests deleting a post by a non-author user. | Aborts with HTTP 403 Forbidden. Post remains in DB. | **PASS** |

---

### Module 3: Commenting System (`tests/test_comments.py`)

| Test Case | Description | Expected Result | Status |
| :--- | :--- | :--- | :---: |
| `test_add_comment_authenticated` | Tests submitting a comment while logged in. | Comment created, linked to user and post, rendered on post page. | **PASS** |
| `test_add_comment_unauthenticated` | Tests submitting a comment as an unauthenticated guest. | Redirected to login page with warning flash. | **PASS** |
| `test_delete_comment_by_author` | Tests deleting a comment by its author. | Comment removed from database; flash message confirms. | **PASS** |
| `test_delete_comment_unauthorized` | Tests deleting a comment by an unrelated user. | Aborts with HTTP 403 Forbidden. | **PASS** |
| `test_post_author_moderation` | Tests post author deleting any comment on their post. | Comment deleted successfully (moderation privilege). | **PASS** |

---

### Module 4: Search and Multi-Filtering (`tests/test_search.py`)

| Test Case | Description | Expected Result | Status |
| :--- | :--- | :--- | :---: |
| `test_search_by_title` | Queries `/?q=Async` across test dataset. | Matches post with "Async" in title; excludes others. | **PASS** |
| `test_search_by_content` | Queries `/?q=RESTful` matching article body content. | Matches post containing "RESTful" in content text. | **PASS** |
| `test_filter_by_category` | Filters `/?category=tutorials`. | Returns only posts associated with "tutorials" category. | **PASS** |
| `test_filter_by_tag` | Filters `/?tag=flask`. | Returns only posts associated with the "flask" tag. | **PASS** |
| `test_combined_search_and_category` | Compound query: `/?q=Python&category=technology`. | Returns only posts matching both keyword and category. | **PASS** |
| `test_search_no_results` | Queries non-existent keyword `/?q=NonExistentKeywordXYZ`. | Returns 200 with "No articles found" empty-state UI. | **PASS** |

---

## 4. Security & Edge Case Validations

1. **Cross-Site Scripting (XSS):**
   - User-supplied Quill HTML passed through `clean_html()` in `app/utils.py`.
   - `<script>alert('xss')</script>` is stripped to safe text.
2. **CSRF Verification:**
   - Active in development and production via `Flask-WTF`.
3. **Database Integrity:**
   - Deleting a `Post` triggers cascade delete for all linked `Comment` records.
   - Deleting a `Post` leaves `Tag` and `Category` intact while clearing association entries in `post_tags`.

---

## 5. Conclusion

All 27 automated test cases run cleanly with zero failures. The application fulfills all quality assurance metrics specified for Week 7 of the DIYInternship program.
