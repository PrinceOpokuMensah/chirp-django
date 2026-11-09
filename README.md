# Chirp – Mini Social Media App (Django)

Features: user profiles (bio + avatar URL), posts, comments, AJAX likes,
follow/unfollow, home feed (people you follow + you), explore page, admin.
DB: SQLite (users, profiles, posts, comments, likes, followers).

## Run
```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations feed
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ — register 2+ accounts to try following and the feed.
