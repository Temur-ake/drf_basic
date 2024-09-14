mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
app:
	python manage.py startapp apps

run:
	python3 manage.py runserver
sup:
	python3 manage.py createsuperuser
build:
	docker build -t new_image_1 .
container:
	docker run -p 8000:8000 -d new_image_1

compose:
	docker compose up --build

down:
	docker compose down

cov:
	pytest --cov-report html --cov


build_index:
	python manage.py search_index --rebuild