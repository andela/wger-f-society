release: invoke create_settings --settings-path /home/wger/wger/settings.py --database-path /home/wger/wger/database.sqlite
release: invoke bootstrap_wger --settings-path /home/wger/wger/settings.py --no-start-server

web: gunicorn wger.wsgi:application