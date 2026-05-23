# Deploy Todomanager with Neon PostgreSQL

This project is configured to use Neon PostgreSQL through `DATABASE_URL`.

## 1. Create the Neon database

1. Go to https://neon.tech and create a project.
2. Open **Connection details**.
3. Copy the pooled connection string for Django/Python.
4. Make sure the URL includes `sslmode=require`.

Example format:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST.neon.tech/DBNAME?sslmode=require
```

## 2. Set deployment environment variables

Set these variables on Render or your deployment platform:

```env
DEBUG=false
SECRET_KEY=<generate-a-long-random-secret>
ALLOWED_HOSTS=your-app.onrender.com,your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com,https://your-domain.com
DATABASE_URL=<your-neon-pooled-connection-string>
DB_SSL_REQUIRE=true
```

Do not set `USE_SQLITE=1` in production.

## 3. Deploy

The included `build.sh` installs dependencies, collects static files, and runs migrations:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

The app starts with:

```bash
gunicorn todomanager.wsgi:application
```

## 4. Test locally with Neon

In PowerShell:

```powershell
$env:DEBUG='false'
$env:DATABASE_URL='postgresql://USER:PASSWORD@HOST.neon.tech/DBNAME?sslmode=require'
python manage.py migrate
python manage.py runserver
```