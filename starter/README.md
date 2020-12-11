# Capstone Casting Agency

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup

With Postgres running, restore a database using the agency.psql file provided:

```bash
python manage.py db init
python manage.py db upgrade
psql -U postgres agency < agency.psql
```

## Authentication - Roles
- Casting Assistant
    Can view actors and movies
- Casting Director
    All permissions a Casting Assistant has and Add or delete an actor from the database Modify actors or movies
- Executive Producer
    All permissions a Casting Director has and Add or delete a movie from the database


## Running the server

First ensure you are working using your created virtual environment. To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Heroku
https://git.heroku.com/agency-fsdn.git


## Endpoint 

GET '/actors'
GET '/movies'
DELETE '/actors/<int:actor_id>'
DELETE '/movies/<int:movie_id>'
POST '/actors'
POST '/movies'
PATCH '/actors/<int:actor_id>'
PATCH '/movies/<int:movie_id>'

```
GET '/actors'
- Fetches a dictionary of actors in which the keys are the ids and the value is name, age, and gender
- Request Arguments: None
- Returns: 1- Success is true, 2- actors_list object
{
    "actors": {
        "1": [
            "Jennifer Aniston",
            30,
            "female"
        ],
        "2": [
            "Courteney Cox",
            56,
            "female"
        ]
    }
}

```
GET '/movies'
- Fetches a dictionary of movies in which the keys are the ids and the value is title and date
- Request Arguments: None
- Returns: 1- Success is true, 2- movies_list object
{
    "movies": {
        "1": [
            "Unknown",
            "September 12, 2005"
        ],
        "2": [
            "Little Women",
            "December 7, 2019"
        ]
    }
}

```
DELETE '/actors/<int:actor_id>'
- Delete an actor 
- Request Arguments: actor_id
- Returns: 1- Success is True. 2- deleted actor id
{
    "deleted": 2,
    "success": true
}

```
DELETE '/movies/<int:movie_id>'
- Delete a movie 
- Request Arguments: movie_id
- Returns: 1- Success is True. 2- deleted movie id
{
    "deleted": 2,
    "success": true
}

```
POST '/actors'
- Fetches the user's input (name, age, gender), add the new actor to the database 
- Request Arguments: None
- Returns: 1- Success is True. 2- created actor id. 3- number of actors 
{
    "created": 7,
    "success": true,
    "totalActors": 6
}

```
POST '/movies'
- Fetches the user's input (title, date), add the new movie to the database 
- Request Arguments: None
- Returns: 1- Success is True. 2- created movie id. 3- number of movies 
{
    "created": 5,
    "success": true,
    "totalMovies": 4
}

```

PATCH '/actors/<int:actor_id>'
- Fetches the user's input (age), edit the existing actor
- Request Arguments: None
- Returns: 1- Success is True. 2- edited actor id. 3- the new age 
{
    "age": 20,
    "id": 1,
    "success": true
}

```

PATCH '/movies/<int:movie_id>'
- Fetches the user's input (title), edit the existing movie
- Request Arguments: None
- Returns: 1- Success is True. 2- edited movie id. 3- the new title 
{
    "id": 1,
    "success": true,
    "title": "New title"
}

```

## Testing
To run the tests, run
```
dropdb agency
createdb agency
python manage.py db upgrade
psql agency < agency.psql
python test_app.py
```

Test the endpoints with [Postman](https://getpostman.com).
 - Import the postman collection `./starter/agency.postman_collection.json`
