# Steps to set up dev environment


1. create venv (Optional)
```
python3 -m venv venv
source venv/bin/activate
```

2. install requirements.txt

```
pip install -r requirements.txt

```
3.Add google creds as env variables

```
export GOOGLE_CLIENT_ID
export GOOGLE_CLIENT_SECRET
```

3.2. Add Hot reload (Optional)
```
export FLASK_ENV=development
```

4. try running the thingy
```

export FLASK_APP=prject.py
flask run 
OR 
gunicorn -b 0.0.0.0:8000 app:app 
( gunicorn for prod server)

```

5. Get migrations in place. this is using sqlite 
 
 ```
flask db init
flask db migrate -m "tables" // idk if you need this line but whatever
flask db upgrade 
```

hopefully should work
