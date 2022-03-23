# Local Setup
- Clone the project
- Run `local_setup.sh`

# Local Development Run
- `local_run.sh` It will start the flask app in `development`. Suited for local development

# Folder Structure

- `db_directory` has the sqlite DB. It can be anywhere on the machine. Adjust the path in ``application/config.py`. Repo ships with one required for testing.
- `application` is where our application code is
- `local_setup.sh` set up the virtualenv inside a local `.env` folder. Uses `pyproject.toml` and `poetry` to setup the project
- `local_run.sh`  Used to run the flask application in development mode
- `static` - default `static` files folder. It serves at '/static' path. 
- `templates` - Default flask templates folder

