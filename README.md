# bike-shop

## List of Contents
1. [Project Requirements](https://github.com/zarifmahfuz/bike-shop/blob/main/docs/requirements.md)
2. [REST API Specification](https://zarifmahfuz.github.io/bike-shop/)
3. Setup
4. Django Intro
5. Potential for Future Improvements

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
Hello World

## Potential For Future Improvements
Hello World
