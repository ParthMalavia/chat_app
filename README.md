# social_media_app

## Steps to django installation

1. Install python3, pip and virtualenv
2. Create a virtual environment by `python3 -m venv myvenv`
3. Activate virtual environment by `source myvenv/bin/activate`
4. Install requirements by `pip install -r requirements.txt`
5. Create database `python manage.py migrate`
6. Create superuser `python manage.py createsuperuser`
7. Run Django by `python manage.py runserver`

## Steps to install redis server

1. Install redis-server by `sudo apt-get install redis-server`
2. Verify port in settings.py file like `REDIS_PORT = 6379`
3. Run redis-server by `sudo systemctl start redis-server`

## Steps to install frontend app (react JS)

1. Install node and npm
2. Go to frontend directory `cd frontend`
3. Run `npm install` to install all dependencies
4. Run `npm start` to run app

## Steps to run both backend and frontend part

1. Open two terminals
2. In first terminal run `python manage.py runserver`
3. In second terminal run `npm start`
