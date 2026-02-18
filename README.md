# Uganda Basketball Registration (No Payment)

## Features
- Public registration form (full fields)
- QR code generation
- PDF receipt generation with logo
- Admin dashboard (view/delete/download PDF)
- SQLite database
- Ready for deployment on Render

## Setup

1. Clone repository
2. Install requirements: `pip install -r requirements.txt`
3. Set environment variable: `FLASK_SECRET_KEY=<your_secret_key>`
4. Run locally: `python app.py`
5. Deploy on Render using `gunicorn app:app`

## Admin Credentials
- Username: admin
- Password: admin123
