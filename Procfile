release: invoke create_settings --settings-path /app/wger/settings.py --database-path /app/wger/database.sqlite
release: invoke bootstrap_wger --settings-path /app/wger/settings.py --no-start-server
web: gunicorn wger.wsgi:application