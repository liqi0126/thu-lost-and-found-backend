# THU Lost and Found Backend

## Setup
```shell script
pip install -r requirements.txt
python manage.py migrate
```
### Sample env
```
APP_ENV=local
APP_SECRET_KEY=your_secret_key
APP_DEBUG=true
APP_URL=http://lostandfound.local

DB_CONNECTION=django.db.backends.mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=lost_and_found_db
DB_USERNAME=root
DB_PASSWORD=secret
```
