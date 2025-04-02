web: gunicorn ecomproject.wsgi --log-file -
web: python manage.py migrate core && gunicorn ecomproject.wsgi