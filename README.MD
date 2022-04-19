Idk start here

1. create venv if you want
```
python3 -m venv venv
source venv/bin/activate
```

2. install requirements.txt

```
pip install -r requirements.txt

```

3. try running the thingy
```

export FLASK_APP=prject.py
flask run 
OR 
gunicorn -b 0.0.0.0:8000 app:app 
( gunicorn for prod server)

```

4. Get migrations in place. this is using sqlite 
 
 ```
flask db init
flask db migrate -m "tables" // idk if you need this line but whatever
flask db upgrade 
```

hopefully should work
