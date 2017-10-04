release: wger create_settings
release: wger migrate_db
release: wger bootstrap
web: gunicorn wger.wsgi:application