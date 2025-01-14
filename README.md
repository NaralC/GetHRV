# Getting Started!

0. Make sure you have Python installed. Version 3.11 was tested to work.
1. `pip install -r requirements.txt` & `python -m pip install Django heartpy neurokit2 pandas`
2. `python manage.py createsuperuser` to create an admin account for Django. Feel free to bypass password security measures here.
    > admin@test.com 1234
3. `python manage.py runserver 0.0.0.0:8000` to start the Django server. The `0.0.0.0` would allow communication from all network interfaces, in this case, the watch. Go to `http://127.0.0.1:8000/hrv/` if `0.0.0.0:8000` does not work.
4. In `mysite\settings.py` — add your development machine IPV4 address to line 28 to allow communicate from the watch. Note that your IPV4 may change from time to time.
5. `python manage.py flush` if you want to wipe the DB.

### Note that running the web server along with the watch app for a few minutes would cause 500 errors to come through; this is due to an unknown error in the web server.