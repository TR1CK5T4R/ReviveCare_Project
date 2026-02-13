# Django Configuration Changes

You mentioned you don't know Django, so here are the **exact changes** you need to make to your Django code.

## File: `/Users/singlatushar/ReViveCare/ReviveCare/ReviveCare/settings.py`

Make these 3 changes:

### Change 1: Add CORS Middleware (Line 49-57)

Find this section:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
```

Add `'corsheaders.middleware.CorsMiddleware',` right after `SecurityMiddleware`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # ← ADD THIS LINE
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### Change 2: Add CSRF Trusted Origins (After Line 47)

Find this line:
```python
CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'http://localhost:5174']
```

Add these two lines right after it:

```python
CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'http://localhost:5174']
CSRF_TRUSTED_ORIGINS = ['http://localhost:5173', 'http://localhost:5174']  # ← ADD THIS
CORS_ALLOW_CREDENTIALS = True  # ← ADD THIS
```

### Change 3: Add Session Settings (At the very end of file)

Go to the end of the file (after line 135) and add:

```python
# Session settings for React frontend
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
```

## That's it!

These are the ONLY changes needed in Django. Save the file and restart your Django server.

## How to Restart Django Server

1. Stop the current server (press `Ctrl+C` in the terminal)
2. Start it again:
   ```bash
   python manage.py runserver
   ```

Your Django backend is now ready to work with React!
