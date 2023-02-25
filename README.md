# bike-shop

## List of Contents
1. [Project Requirements](https://github.com/zarifmahfuz/bike-shop/blob/main/docs/requirements.md)
2. [REST API Specification](https://zarifmahfuz.github.io/bike-shop/)
3. Setup
4. Django Intro
5. More Features

## REST API
I developed an OpenAPI specification before implementing the REST APIs for this application. The API specification can be viewed here: https://zarifmahfuz.github.io/bike-shop/.

## Setup
### System Requirements
* Python 3.7-3.11
* Node v16+
* Sqlite3

### Backend
1. Start a new virtual environment:
```
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
2. Install dependencies with `pip install -r requirements.txt`
3. Run the database migrations with `python3 manage.py migrate`
4. Load the seed data for the app with `python3 manage.py loaddata seed_data.json`
5. Run the server with `python3 manage.py runserver`. This runs the server on port `8000` by default. If you want to run the server on a different port, run `python3 manage.py runserver <port>`

### Frontend
1. `cd frontend`
2. `npm install`
3. Run the frontend server with `npm run dev`. You should see the url from which you can finally run the application! :tada:
4. Note that if you changed the backend server port, you will need to change the `SERVER_PORT` variable in [`frontend/config.ts`](https://github.com/zarifmahfuz/bike-shop/blob/main/frontend/config.ts) to match your server's port.

## Django Intro
If you are unfamiliar with Django, the following is meant to give you a very high-level overview of files in `backend/`, in order to make it a little easier for you navigate through the codebase.
1. `urls.py`: This is the entry point to the backend.
2. `models.py`: This defines all the entitires for the application and implements parts of the business logic.
3. `managers.py`: This implements the other parts of the business logic. The difference between `managers.py` and `models.py` is that `managers.py` operates over the entire entity and `models.py` operates over a single instance of the entity.
4. `views.py`: This connects the API endpoints to the backend logic and returns HTTP responses.
5. `serializers.py`: This defines the input and output serializers for the API.
6. `tests`: This defines the automated tests for the app.

## Potential For More Features
This is a MVP of the app that I built in a few days! There are so many more things that I would wish to implement over time. Some of them are listed below!
1. Implement pagination for the Sales and Bikes pages
2. Implement user management, authorization and authentication
3. Add database indexes to make the app more performant
4. Etc.
