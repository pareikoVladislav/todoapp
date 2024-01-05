migrate:
	python manage.py makemigrations
	python manage.py migrate

createuser:
	python manage.py createsuperuser

run:
	python manage.py runserver

collect_static:
	python manage.py collectstatic
