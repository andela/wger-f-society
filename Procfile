release: invoke create_settings --settings-path /app/settings.py
release: invoke migrate_db
release: invoke bootstrap-wger --settings-path /app/settings.py --no-start-server
web: gunicorn wger.wsgi:application