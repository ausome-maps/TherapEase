#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres... $SQL_HOST $SQL_PORT;"

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate

{
  python manage.py shell -c "from django.contrib.auth.models import User;
if not User.objects.filter(email='admin@sample.com').exists(): User.objects.create_superuser('admin@sample.com', 'admin@sample.com', 'adminpassword012')" &>/dev/null
  echo "user admin@sample.com created with password adminpassword012"
} || { 
  echo "user admin@sample.com exists!"
}
exec "$@"
