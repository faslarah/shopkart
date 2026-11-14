#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create a superuser if it doesn't exist
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin123').exists() or User.objects.create_superuser('admin123', 'admin@openmall.com', 'admin123')"

python manage.py shell -c "from store.models import Product; Product.objects.exists() or __import__('subprocess').run(['python', 'manage.py', 'loaddata', 'fixtures/initial_data.json'])"