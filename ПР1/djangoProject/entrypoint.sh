#!/bin/bash

python /code/docere/manage.py migrate

python /code/docere/manage.py collectstatic --noinput

chown -R www-data:www-data /code/docere/media

# Создаём суперпользователя
if [ "${CREATE_SUPERUSER:-true}" = "true" ]; then
python /code/docere/manage.py shell <<'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin")
    print("Суперпользователь создан: admin / admin")
else:
    print("Суперпользователь уже существует")
EOF
fi

# сидим демо-врачей только когда явно попросили
if [ "${SEED_DEMO:-false}" = "true" ]; then
  python /code/docere/manage.py seed_demo --doctors=${DEMO_DOCTORS:-3}
fi

exec "$@"