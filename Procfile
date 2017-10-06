release: invoke create-settings --settings-path /app/settings.py
release: invoke bootstrap-wger --settings-path /app/settings.py --no-start-server
release: invoke bootstrap-wger
web: gunicorn wger.wsgi:application