# Social Distribution - a CMPUT404 Project

# Local Setup

1. Run `docker-compose up` to spin up your local postgres server. If you want to access the database from a database browser, here are the details:
   - Host: localhost
   - Port: 5432
   - Database: postgres
   - Username: admin
   - Password: root
2. Run `python manage.py migrate` to apply migration to the postgres
3. Create a copy of the `.env.example` and name it `.env`. Populate the env file (add a secret key)
   - If you want to test locally but use the heroku test db, change `TEST` to `TRUE`
4. Create a virtualenv in the root folder, then run `pip install -r requirements.txt`
5. Run `heroku local` for non window user to start the server. Access it at `http://localhost:8000`
   - Window doesn't support gunicorn so you'll have to do `heroku local -f Procfile.window`

# Create superuser on Heroku
- Local: Run `python manage.py create_admin`
- Heroku: Run `heroku run -a social-dist-wed python manage.py create_admin`

# Deployment to Heroku

Deployment to Heroku will use PostgreSQL

1. Install heroku cli and login
