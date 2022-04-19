Idk start here

source venv/bin/activate
export FLASK_APP=prject.py
flask db init
flask db migrate -m "tables" // idk if you need this line but whatever
flask db upgrade