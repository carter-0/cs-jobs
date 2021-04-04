import os

### Calls system to run gunicorn and start main.py ###

os.system('gunicorn --bind 0.0.0.0:8080 main')
