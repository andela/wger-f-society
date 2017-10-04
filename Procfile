release: invoke create_settings --settings-path wger/settings.py --database-path wger/database.sqlite
release: invoke bootstrap_wger --settings-path wger/settings.py --no-start-server
web: gunicorn wger.wsgi:application