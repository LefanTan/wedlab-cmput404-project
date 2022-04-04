web: gunicorn social_distribution.wsgi
release: python manage.py migrate auth
release: python manage.py create_admin