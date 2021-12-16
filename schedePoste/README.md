### create env
python3 -m venv venv

### activate env
. venv/bin/activate


### initialize app
export FLASK_APP=schedePoste
export FLASK_ENV=development
flask run

### initialize db
flask init-db
