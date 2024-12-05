# Weird Stack Challenge Website

This project is a challenge to create a complete website using a unique stack combination:

- **HTMX** for frontend interactions
- **Jinja Templates** for HTML rendering
- **FastAPI** as the backend framework
- **PostgreSQL** as the database
- **SQLAlchemy** for ORM
- **Websockets** for real-time group chat functionality

## Features

1. **Authentication Pages**  
   - Login and Register pages built with HTMX and Jinja templates.
   
2. **Group Chat**  
   - A real-time chat page using Websockets, with HTMX handling dynamic content updates.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set the database URL:  
   Open `models.py` and update the `DATABASE_URL` with your PostgreSQL connection string.

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

5. Access the application at:
   ```
   http://127.0.0.1:8000
   ```

## Project Structure
```
python-htmx
├── auth_router.py
├── db.py
├── dependency.py
├── main.py
├── models.py
├── readme.md
├── requirements.txt
├── schema.py
└── static
    ├── images
    │   ├── bg.jpg
    │   ├── logo.png
    │   └── welcome.png
    ├── index.html
    ├── stylesheets
    │   ├── style.css
    │   ├── style.css.map
    │   └── style.scss
    └── templates
        ├── about.html
        ├── auth.html
        ├── errors.html
        ├── home.html
        ├── login.html
        ├── message.html
        └── register.html
```

## Weird Stack, Cool Experience!

Enjoy exploring this unconventional tech stack for a fun, fully functional website!
