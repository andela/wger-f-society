release: python manage.py makemigrations
release: python manage.py migratedb
release: python manage.py createcachetable
web: gunicorn wger.wsgi:application