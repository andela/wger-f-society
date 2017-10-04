release: wger create_settings
release: wger migrate_db
release: wger bootstrap_wger
web: gunicorn wger.wsgi:application