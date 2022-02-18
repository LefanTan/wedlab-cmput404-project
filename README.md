# Social Distribution - a CMPUT404 Project

# Local Setup

1. Run `python manage.py migrate` to apply migration to the sqlite3 db
2. Create a copy of the `.env.example` and name it `.env`. Populate the env file (add a secret key)
3. Create a virtualenv in the root folder, then run `pip install -r requirements.txt`
4. Run `heroku local` for non window user to start the server. Access it at `http://localhost:8000`
   - Window doesn't support gunicorn so you'll have to do `heroku local -f Procfile.window`

# Deployment to Heroku

Deployment to Heroku will use PostgreSQL

1. Install heroku cli and login
