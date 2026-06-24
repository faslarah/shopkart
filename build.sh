#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create or update superuser password
python manage.py shell -c "from django.contrib.auth.models import User; u, _ = User.objects.get_or_create(username='admin123'); u.set_password('admin123'); u.is_superuser=True; u.is_staff=True; u.save()"
