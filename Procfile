release: invoke create_settings --settings-path /app/wger/settings.py
release: invoke migrate_db
release: invoke bootstrap_wger --settings-path /app/wger/settings.py --no-start-server
web: gunicorn wger.wsgi:application