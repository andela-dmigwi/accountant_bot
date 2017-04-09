# 	Created by Migwi Ndung'u 
#   @ The Samurai Community 2017

python manage.py db init
python manage.py db migrate
python manage.py db upgrade
gunicorn manage:app --log-file=-