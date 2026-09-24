# Alzikrayat — Full Project Implementation Plan

> **Course:** Advanced Web Technologies  
> **Project:** Alzikrayat Photo Sharing Web Application  
> **Backend:** Python + Flask  
> **Database:** MySQL + PyMySQL  
> **Frontend:** HTML5 + Bootstrap + Custom CSS + Vanilla JavaScript  
> **Architecture:** MVC + 3-Tier  
> **Goal:** Build a simple, modern, professional project that follows the course specification closely without unnecessary features.

---

# 1. Project Goal

Build **Alzikrayat**, a simple photo-sharing web application where users can:

- Register an account.
- Login and logout.
- Upload photos.
- Browse uploaded photos in a gallery.
- Open a photo details page.
- Add comments to photos.
- Like / unlike photos.
- Tag registered users in uploaded photos.
- Delete only their own photos.
- View their own uploaded photos.
- Switch gallery display style.
- View a simple About page.

The priority is **correct architecture and compliance with the assignment**, not building a large social network.

The application should look modern and polished, but remain simple enough to implement, explain, and maintain.

---

# 2. Important Scope Decisions

## 2.1 Backend

Use:

- Python
- Flask
- PyMySQL
- MySQL

Do **not** use:

- SQLAlchemy
- Flask-SQLAlchemy
- Any ORM
- Django
- FastAPI
- External backend frameworks
- Complex frontend frameworks such as React/Vue

All SQL must be written manually using parameterized queries.

---

## 2.2 Routing Decision

Follow the **Python Flask routing example from the course specification**.

Flask route decorators may be used as thin request listeners:

```python
@app.route("/photo/<int:photoId>", methods=["GET"])
def showPhoto(photoId):
    from app.controllers.photo_controller import PhotoController
    return PhotoController.show(photoId)
```

The route must **only delegate to a Controller**.

Do not put:

- SQL
- business rules
- validation logic
- template logic
- ownership checks

inside `routes.py`.

Correct flow:

```text
Browser
  ↓
Flask Route Listener
  ↓
Controller
  ↓
Model
  ↓
MySQL
  ↓
Controller
  ↓
View
```

This matches the assignment's Python blueprint while keeping MVC separation clear.

---

# 3. Architecture

Use both **MVC** and **3-Tier Architecture**.

## 3.1 MVC

### Model

Responsible for:

- Database queries.
- Mapping rows to data structures.
- Data-specific operations.
- Raw SQL.
- Database validation where appropriate.

Examples:

```text
User
Photo
Comment
PhotoLike
PhotoTag
```

### View

Responsible for:

- HTML.
- Bootstrap layout.
- Displaying data passed by Controllers.
- Simple template conditions.
- Escaped output.

Views must not perform SQL.

### Controller

Responsible for:

- Receiving requests from routes.
- Reading form data.
- Calling validators.
- Calling Models.
- Checking sessions.
- Checking ownership.
- Redirecting or rendering templates.
- Coordinating the application.

---

## 3.2 Three-Tier Mapping

```text
Presentation Tier
├── HTML templates
├── Bootstrap
├── CSS
└── JavaScript

Application / Business Tier
├── routes.py
├── Controllers
├── Session/Auth logic
└── Validators

Data Tier
├── Models
├── Database connection
└── Raw parameterized SQL
```

---

# 4. Project Structure

Use a clear structure close to the course Flask example.

```text
alzikrayat/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes.py
│   │
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── home_controller.py
│   │   ├── photo_controller.py
│   │   ├── comment_controller.py
│   │   ├── like_controller.py
│   │   └── tag_controller.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── photo.py
│   │   ├── comment.py
│   │   ├── photo_like.py
│   │   └── photo_tag.py
│   │
│   ├── validators/
│   │   ├── auth_validator.py
│   │   ├── photo_validator.py
│   │   └── comment_validator.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── views/
│   │   └── templates/
│   │       ├── layout/
│   │       │   └── base.html
│   │       │
│   │       ├── auth/
│   │       │   ├── login.html
│   │       │   └── register.html
│   │       │
│   │       ├── photos/
│   │       │   ├── index.html
│   │       │   ├── show.html
│   │       │   ├── create.html
│   │       │   └── my_photos.html
│   │       │
│   │       ├── home.html
│   │       └── about.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       ├── js/
│       │   ├── validation.js
│       │   └── gallery.js
│       │
│       └── uploads/
│
├── database/
│   └── schema.sql
│
├── run.py
├── requirements.txt
├── README.md
└── .gitignore
```

Keep the structure understandable and easy to explain during the TA demonstration.

---

# 5. Database

Use **MySQL**, not SQLite, because MySQL is the database standard stated in the project specification.

Use:

```text
PyMySQL
```

Do not use any ORM.

---

# 6. Database Schema

The three required core tables are:

- `users`
- `photos`
- `comments`

Two additional tables are added for novelty features:

- `photo_likes`
- `photo_tags`

---

## 6.1 users

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    location VARCHAR(100) NULL,
    description TEXT NULL,
    occupation VARCHAR(100) NULL
);
```

Rules:

- First name required.
- Last name required.
- Email required and unique.
- Password stores only a secure hash.
- Location optional.
- Description optional.
- Occupation optional.

---

## 6.2 photos

```sql
CREATE TABLE photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NULL,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_photos_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
```

Rules:

- Uploaded image is physically stored in `app/static/uploads/`.
- Database stores only metadata and file name/path.
- A photo belongs to one user.

---

## 6.3 comments

```sql
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    photo_id INT NOT NULL,
    user_id INT NOT NULL,
    comment TEXT NOT NULL,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_comments_photo
        FOREIGN KEY (photo_id)
        REFERENCES photos(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_comments_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
```

Comments should display in chronological order by default.

Suggested query:

```sql
ORDER BY comments.date_time ASC
```

Do not add comment sorting UI unless needed later.

---

## 6.4 photo_likes

Novelty feature.

```sql
CREATE TABLE photo_likes (
    photo_id INT NOT NULL,
    user_id INT NOT NULL,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (photo_id, user_id),

    CONSTRAINT fk_likes_photo
        FOREIGN KEY (photo_id)
        REFERENCES photos(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_likes_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
```

The composite primary key ensures:

```text
one user → one like per photo
```

Like action should behave as a toggle:

```text
Not liked → Like
Liked     → Unlike
```

---

## 6.5 photo_tags

Novelty feature.

```sql
CREATE TABLE photo_tags (
    photo_id INT NOT NULL,
    user_id INT NOT NULL,

    PRIMARY KEY (photo_id, user_id),

    CONSTRAINT fk_tags_photo
        FOREIGN KEY (photo_id)
        REFERENCES photos(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_tags_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
```

Purpose:

A photo can tag multiple registered users.

Example:

```text
Photo 10
├── Ahmed
├── Sara
└── Mohamed
```

No hashtags are required.

---

# 7. Pages

Keep the application pages limited and clear.

---

## 7.1 Home / Landing Page

Route:

```text
GET /
```

Purpose:

A welcoming project landing page.

Must include:

- Alzikrayat branding/logo.
- Simple hero section.
- Short project description.
- A few recent photos.
- Basic statistics.
- Clear navigation.
- Link to gallery.
- Link to About.

Possible statistics:

```text
Photos
Users
Comments
Likes
```

Do not make the homepage crowded.

### Logged-out state

Navbar:

```text
Alzikrayat | Home | Photos | About | Please Login
```

Buttons may include:

```text
Get Started
View Photos
```

### Logged-in state

Navbar:

```text
Alzikrayat | Home | Photos | Upload | About | Hi Ahmed | Logout
```

Hero can change slightly:

```text
Welcome back, Ahmed
Share a new memory or explore photos.
```

---

# 8. Login Page

Route:

```text
GET  /login
POST /login
```

Fields:

```text
Email
Password
```

Required behavior:

- Validate email.
- Verify password hash.
- Start session.
- Store required session values.
- Set last-login cookie.
- Redirect to homepage/gallery.

Display:

```text
Last login from this computer was:
[Timestamp]
```

The cookie must expire after **7 days**.

Do not add unnecessary functionality such as:

- OAuth
- Google login
- Forgot password flow

unless explicitly requested later.

---

# 9. Register Page

Route:

```text
GET  /register
POST /register
```

Fields:

```text
First Name
Last Name
Email
Password
Confirm Password
Location        optional
Occupation      optional
Description     optional
```

The simple UI may initially show only the important fields prominently and place optional fields below them.

Validation:

- Required first name.
- Required last name.
- Valid email.
- Unique email.
- Password minimum length.
- Password confirmation.
- Server-side validation for everything.

Hash password before saving.

Never save raw passwords.

---

# 10. Gallery Page

Route:

```text
GET /photos
```

Purpose:

Display all uploaded photos.

Each card should show only useful information:

```text
Photo
Title
Uploader
Like count
Comment count
```

Do not include:

- Search
- Follow buttons
- Share buttons
- Hashtags
- Similar Photos
- Category tags
- Complex filters

The project should remain simple.

---

## 10.1 Gallery Display Styles

The specification requires custom display styles.

Implement two modes:

```text
Grid
List
```

Optional:

```text
3-column grid
4-column grid
```

This can be handled client-side with Bootstrap classes and JavaScript.

No database change is required.

Example:

```text
[ Grid ] [ List ]
```

Remember the user's selected display mode only if easy; it is not required.

---

## 10.2 Optional Sorting

Sorting is acceptable as a small UX feature.

Possible options:

```text
Newest
Oldest
Most Liked
Most Commented
```

Keep this simple.

No search bar.

---

# 11. Photo Details Page

Route:

```text
GET /photo/<int:photoId>
```

This is one of the most important pages.

Layout:

```text
Large Photo

Title
Uploader
Date
Description

Like button + Like count

Tagged People

Comments

Comment form
```

---

## 11.1 Photo Metadata

Display:

- Large photo.
- Title.
- Author.
- Upload date.
- Description.

Do not include:

- Similar Photos.
- Share.
- Follow.
- Hashtags.
- Unrelated social media features.

---

## 11.2 Likes

Display:

```text
♡ 12 Likes
```

or if liked:

```text
♥ 12 Likes
```

Clicking should toggle the like.

Only authenticated users can like.

Prefer simple POST + redirect behavior first.

AJAX is optional, not required.

Routes:

```text
POST /photo/<int:photoId>/like
```

The Controller decides whether to:

```text
insert like
```

or:

```text
delete like
```

based on whether the current user already liked the photo.

---

## 11.3 Tagged People

Display simple registered-user tags:

```text
Tagged People

[ Sara Ahmed ] [ Mohamed Ali ]
```

No hashtag system.

---

## 11.4 Comments

Show comments in chronological order:

```text
Oldest
↓
Newest
```

Each comment displays:

```text
User Name
Timestamp
Comment Text
```

At bottom:

```text
[ Write a comment... ] [ Post ]
```

Do not add comment sorting.

Do not add nested replies unless explicitly requested later.

---

# 12. Upload Photo Page

Routes:

```text
GET  /photo/upload
POST /photo/store
```

Only authenticated users can access this page.

Fields:

```text
Image
Title
Description
Tag People (optional)
```

UI:

```text
Image drop/select area

Title
Description
Tagged Users

Upload Photo
```

Do not implement image filters.

---

## 12.1 Upload Rules

Validate:

- File exists.
- File type is allowed.
- File size is acceptable.
- Title is present.
- User is authenticated.

Suggested formats:

```text
.jpg
.jpeg
.png
.webp
```

Use secure generated filenames to avoid collisions.

Example:

```text
uuid + extension
```

Do not trust the original user filename.

---

# 13. My Photos Page

Route:

```text
GET /my-photos
```

Purpose:

Show photos uploaded by the current user.

Each card may contain:

```text
Image
Title
Date
Likes
Comments
More menu
```

Actions:

```text
Open
Delete
```

Do not build a large profile system.

This page is enough for managing uploaded photos.

---

# 14. Delete Photo

Route:

```text
POST /photo/<int:photoId>/delete
```

Critical security rule:

Before deleting:

```text
photo.user_id == session.userId
```

If false:

```text
403 / redirect with error
```

Deletion process:

```text
1. Fetch photo.
2. Confirm ownership.
3. Delete database record.
4. Delete physical file.
5. Cascade removes comments, likes, tags.
6. Redirect to My Photos.
```

Keep database and disk synchronized.

---

# 15. About Page

Route:

```text
GET /about
```

Static page.

Keep it short.

Example content:

```text
Alzikrayat is a photo-sharing web application created as part of the
Advanced Web Technologies course.

The project demonstrates MVC architecture, 3-Tier architecture,
authentication, raw SQL, photo management, comments, likes, and tagging.
```

Simple UI only.

---

# 16. Routes

Keep `routes.py` flat and easy to inspect.

Suggested routes:

```text
GET    /
GET    /about

GET    /login
POST   /login

GET    /register
POST   /register

POST   /logout

GET    /photos

GET    /my-photos

GET    /photo/upload
POST   /photo/store

GET    /photo/<int:photoId>

POST   /photo/<int:photoId>/delete

POST   /photo/<int:photoId>/comment

POST   /photo/<int:photoId>/like

POST   /photo/<int:photoId>/tag
```

Example:

```python
@app.route("/photo/<int:photoId>", methods=["GET"])
def showPhoto(photoId):
    from app.controllers.photo_controller import PhotoController
    return PhotoController.show(photoId)
```

Again:

`routes.py` must remain only a dispatcher.

---

# 17. Controllers

---

## 17.1 HomeController

Methods:

```text
index()
about()
```

`index()` gets:

- latest photos
- photo count
- user count
- comment count
- like count

and sends them to the homepage.

---

## 17.2 AuthController

Methods:

```text
showLogin()
login()
showRegister()
register()
logout()
```

Responsibilities:

- Form input collection.
- Validation.
- Password hashing/verifying.
- Session management.
- Last login cookie.
- Redirects.

---

## 17.3 PhotoController

Methods:

```text
index()
show(photoId)
showUpload()
store()
myPhotos()
delete(photoId)
```

Responsibilities:

- Gallery.
- Photo details.
- Upload.
- Ownership.
- Deletion.
- My Photos.

---

## 17.4 CommentController

Method:

```text
store(photoId)
```

Responsibilities:

- Require authenticated user.
- Validate comment.
- Save comment.
- Redirect back to photo.

---

## 17.5 LikeController

Method:

```text
toggle(photoId)
```

Pseudo logic:

```text
if user already liked photo:
    remove like
else:
    add like
```

Return to the photo page.

---

## 17.6 TagController

Only needed if tagging after upload is implemented as a separate action.

Possible methods:

```text
store(photoId)
remove(photoId, userId)
```

However, simplest implementation is to process selected tags inside `PhotoController.store()`.

Prefer the simpler version unless a separate Controller makes the code clearer.

---

# 18. Models

Each model should contain database-specific code only.

---

## 18.1 User Model

Suggested methods:

```text
findById(userId)
findByEmail(email)
create(...)
emailExists(email)
getAllExcept(userId)
count()
```

---

## 18.2 Photo Model

Suggested methods:

```text
getAll(sort=None)
getLatest(limit)
findById(photoId)
create(...)
delete(photoId)
getByUser(userId)
count()
```

Photo detail query should include author information.

---

## 18.3 Comment Model

Suggested methods:

```text
getByPhoto(photoId)
create(photoId, userId, comment)
countByPhoto(photoId)
count()
```

---

## 18.4 PhotoLike Model

Suggested methods:

```text
hasLiked(photoId, userId)
add(photoId, userId)
remove(photoId, userId)
countByPhoto(photoId)
count()
```

---

## 18.5 PhotoTag Model

Suggested methods:

```text
add(photoId, userId)
remove(photoId, userId)
getUsersForPhoto(photoId)
```

---

# 19. Authentication and Sessions

After successful login:

```python
session["userId"] = user["id"]
session["firstName"] = user["first_name"]
```

Optional:

```python
session["email"] = user["email"]
```

Do not store sensitive data unnecessarily.

---

## 19.1 Login Protection

Write a small reusable helper/decorator if appropriate:

```text
loginRequired
```

Use it for:

```text
Upload
Delete
Comment
Like
My Photos
Tag
```

Do not overengineer the authentication system.

---

# 20. Last Login Cookie

On successful login:

1. Read previous cookie value.
2. Display it on the next login page if available.
3. Set/update cookie with current successful login timestamp.
4. Cookie expiry = 7 days.

Cookie name example:

```text
lastLogin
```

Use sensible flags when possible:

```text
HttpOnly
SameSite=Lax
```

---

# 21. Validation

The project specification requires three validation layers.

Every important form should use:

```text
HTML5
+
JavaScript
+
Python backend validation
```

---

## 21.1 HTML5 Validation

Examples:

```html
required
type="email"
maxlength="100"
minlength="8"
accept="image/*"
```

---

## 21.2 JavaScript Validation

Use custom JavaScript for:

- Empty fields.
- Email shape.
- Password length.
- Password confirmation.
- Comment length.
- File size/type.
- Upload title.

Keep JavaScript simple.

No JS framework.

---

## 21.3 Python Validation

Never trust the browser.

Repeat validation on the backend.

Examples:

```text
valid email
required values
maximum lengths
unique email
safe photo extension
file size
photo exists
user authenticated
ownership
```

---

# 22. Security

At minimum implement:

- Password hashing.
- Parameterized SQL.
- Session authentication.
- Ownership checks.
- Safe uploaded filenames.
- File type checks.
- XSS-safe template output.
- Form input validation.

---

## 22.1 SQL Injection

Never do:

```python
query = "SELECT * FROM users WHERE email = '" + email + "'"
```

Do:

```python
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,)
)
```

All database queries must follow this rule.

---

## 22.2 XSS

Use Jinja automatic escaping.

Do not unnecessarily use:

```text
|safe
```

for user-generated content.

User fields requiring normal escaping include:

```text
Name
Photo Title
Description
Comment
Occupation
Location
```

---

# 23. UI / UX Direction

Design must be:

```text
Simple
Modern
Clean
Professional
Responsive
Not overloaded
```

Use:

- White / very light background.
- Dark text.
- One blue/navy accent.
- Rounded cards.
- Subtle borders/shadows.
- Good spacing.
- Simple icons.
- Large photo areas.
- Clear typography.

Avoid:

- Excessive gradients.
- Excessive animations.
- Large decorative effects.
- Too many colors.
- Fake social-media features.

The result should look like a student-built professional web project, not an overdesigned social network.

---

# 24. Navbar

Logged out:

```text
Alzikrayat
Home
Photos
About
Please Login
```

Logged in:

```text
Alzikrayat
Home
Photos
Upload
About
Hi <firstName>
Logout
```

Keep header compact.

---

# 25. Footer

Keep footer very small.

Example:

```text
© 2026 Alzikrayat
Advanced Web Technologies Project
```

No complex sitemap.

---

# 26. Responsive Design

Bootstrap must be used.

Support:

- Desktop.
- Tablet.
- Mobile.

Use Bootstrap grid and a small number of custom media queries.

Important pages to test:

```text
Home
Gallery
Photo Detail
Upload
Login
Register
```

---

# 27. Novelty Features

The two planned novelty features are:

## Novelty 1 — Likes

Users can:

```text
Like photo
Unlike photo
See number of likes
```

Benefits:

- Easy to demonstrate.
- Adds database interaction.
- Fits the photo-sharing concept.
- Uses a normalized many-to-many relationship.

---

## Novelty 2 — Tag Registered Users

When uploading a photo, user can select registered users to tag.

Photo details display the tagged users.

Benefits:

- Explicitly fits the type of advanced feature suggested by the assignment.
- Demonstrates many-to-many database relationships.
- Makes the project more interesting without creating major complexity.

---

# 28. Features Explicitly Out of Scope

Do **not** implement these unless requested later:

```text
Image filters
Follow system
Private messages
Hashtags
Similar photos
Share buttons
External social media posting
Notifications
Search
Nested comment replies
Stories
Realtime chat
AI features
Albums as a full separate system
Complex user profiles
Admin dashboard
Forgot-password email system
OAuth
```

This is important.

Keep the project focused.

---

# 29. Development Phases

Implement in the following order.

---

## Phase 1 — Project Foundation

Create:

```text
Flask app
Folder structure
requirements.txt
config.py
MySQL connection
base template
routes.py
```

Test:

```text
GET /
GET /about
```

Goal:

The application starts correctly and follows the desired structure.

---

## Phase 2 — Database

Create:

```text
users
photos
comments
photo_likes
photo_tags
```

Add:

```text
foreign keys
cascade deletes
indexes where useful
```

Create initial Models.

Test raw SQL connection.

---

## Phase 3 — Authentication

Implement:

```text
Register
Login
Logout
Password hashing
Sessions
Last login cookie
Dynamic navbar
```

Test all invalid inputs.

---

## Phase 4 — Photo Core

Implement:

```text
Upload photo
Save file
Save metadata
Gallery
Photo details
My Photos
Delete own photo
```

Test disk/database synchronization.

---

## Phase 5 — Comments

Implement:

```text
Add comment
Display comments
Chronological order
Authenticated users only
```

---

## Phase 6 — Likes

Implement:

```text
Like
Unlike
Like count
Like state
```

Use `photo_likes`.

---

## Phase 7 — Tagging

Implement:

```text
Select registered users while uploading
Store photo_tags
Display tagged users
```

Keep tag UI simple.

---

## Phase 8 — Gallery Display Modes

Implement:

```text
Grid
List
```

Optional:

```text
3-column
4-column
```

Use Bootstrap and vanilla JavaScript.

---

## Phase 9 — UI Polish

Apply consistent styling to:

```text
Home
Gallery
Photo details
Upload
Login
Register
About
My Photos
```

Check:

```text
mobile
tablet
desktop
```

---

## Phase 10 — Validation and Security Review

Verify:

```text
HTML5 validation
JS validation
Python validation
SQL injection protection
XSS protection
password hashing
ownership checks
upload safety
```

---

## Phase 11 — Final Testing

Test full user flow:

```text
Register
↓
Login
↓
Upload Photo
↓
Tag User
↓
Open Gallery
↓
Open Photo
↓
Like
↓
Comment
↓
My Photos
↓
Delete Photo
↓
Logout
↓
Login Page shows last login timestamp
```

---

# 30. Error Handling

Handle common cases gracefully.

Examples:

```text
404 — Photo/Page not found
403 — Not allowed
Invalid form
Invalid login
Duplicate email
Invalid upload
Database failure
```

Do not expose raw database errors to the browser.

---

# 31. Documentation Rules

The course specification requires strong code documentation.

Each major:

```text
class
method
function
```

should have a useful comment/docstring describing:

- Purpose.
- Parameters.
- Return value.
- Important errors.

Do not fill the code with obvious comments.

Comments should explain decisions, not restate simple syntax.

---

# 32. Naming Style

Follow the requested style.

Classes:

```text
PascalCase

PhotoController
AuthController
PhotoLike
```

Variables/functions:

```text
camelCase

photoId
userId
lastLoginDate
getPhotoById()
```

Maintain consistency throughout the project.

---

# 33. Git Workflow

The final submission requires a GitHub repository with 10+ commits.

Do not build everything in one commit.

Suggested commit history:

```text
1. Initialize Flask project structure
2. Add MySQL schema and database connection
3. Add registration
4. Add login sessions and logout
5. Add last-login cookie
6. Add photo upload
7. Add gallery and photo details
8. Add comments
9. Add likes
10. Add user tagging
11. Add My Photos and ownership deletion
12. Add responsive UI and validation
13. Add security fixes and cleanup
14. Add README and architecture documentation
```

Commit messages should describe real work.

---

# 34. README

README should include:

```text
Project description
Features
Technology stack
Architecture
Folder structure
Database setup
Installation
Configuration
How to run
Demo account if needed
Security notes
Novelty features
```

---

# 35. Architecture Report

Prepare a short 2–3 page PDF report explaining:

```text
MVC architecture
3-Tier architecture
Request flow
Database schema
Authentication/session approach
Manual/raw SQL approach
Novelty features
Security protections
```

Include a simple flow diagram:

```text
Browser
↓
Flask route
↓
Controller
↓
Model
↓
MySQL
↓
View
```

---

# 36. Final Submission Checklist

Before submission verify:

- [ ] Flask project runs locally without warnings/errors.
- [ ] Routing follows the Python Flask blueprint and delegates to Controllers.
- [ ] MVC separation is clear.
- [ ] 3-Tier separation is explainable.
- [ ] MySQL is used.
- [ ] PyMySQL is used.
- [ ] No ORM exists.
- [ ] All SQL is handwritten.
- [ ] SQL queries are parameterized.
- [ ] Users table exists.
- [ ] Photos table exists.
- [ ] Comments table exists.
- [ ] Photo likes table exists.
- [ ] Photo tags table exists.
- [ ] Cascade deletes work.
- [ ] Registration works.
- [ ] Login works.
- [ ] Logout works.
- [ ] Passwords are securely hashed.
- [ ] Session authentication works.
- [ ] Navbar changes based on auth state.
- [ ] Last-login cookie works for 7 days.
- [ ] Uploads are physically stored.
- [ ] Photo metadata is stored.
- [ ] Gallery works.
- [ ] Gallery display toggle works.
- [ ] Photo details work.
- [ ] Comments work.
- [ ] Likes work.
- [ ] User tagging works.
- [ ] My Photos works.
- [ ] Users cannot delete other users' photos.
- [ ] Photo deletion removes DB record and physical file.
- [ ] HTML5 validation exists.
- [ ] JavaScript validation exists.
- [ ] Python validation exists.
- [ ] Output is escaped against XSS.
- [ ] Bootstrap responsive layout works.
- [ ] Mobile layout works.
- [ ] Tablet layout works.
- [ ] Desktop layout works.
- [ ] README exists.
- [ ] GitHub repository has 10+ meaningful commits.
- [ ] 2–3 page architecture report is ready.

---

# 37. Expected Final Product

The final product should feel like a **small but complete photo-sharing application**.

It should not try to imitate Instagram.

The strength of the project should be:

```text
Correct architecture
+
Clean raw SQL implementation
+
Clear authentication
+
Photo CRUD
+
Comments
+
Likes
+
Tagging
+
Simple modern UI
+
Good validation/security
```

When choosing between adding another feature and making the required architecture clearer, always prioritize the architecture and required specification.

---

# 38. Instruction to the Coding Agent

Build the project incrementally.

Do not implement everything at once.

For each phase:

1. Inspect the existing code.
2. Implement only the current phase.
3. Keep MVC boundaries strict.
4. Do not introduce libraries that violate the specification.
5. Run the application/tests after every meaningful change.
6. Do not add features outside this document without asking.
7. Keep the design simple and consistent.
8. Avoid unnecessary abstractions.
9. Prefer readable student-level code over clever code.
10. Preserve the ability to explain every major part during the TA demonstration.

The project must look professional, but its implementation should remain understandable to a university student.

