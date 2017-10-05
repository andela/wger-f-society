release: invoke bootstrap-wger --settings-path /app/settings.py --no-start-server
web: gunicorn wger.wsgi:application