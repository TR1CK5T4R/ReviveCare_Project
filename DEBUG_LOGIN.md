# Testing Patient Login - Debug Checklist

## Step 1: Verify Patient Was Added to Database

**In Django terminal, run:**
```bash
python manage.py shell
```

Then in the Python shell:
```python
from Patients.models import Patient
patients = Patient.objects.all()
for p in patients:
    print(f"Name: {p.name}, Email: {p.email}")
```

Type `exit()` to exit the shell.

**WRITE DOWN THE EMAIL** that you see - you'll use this exact email to log in.

---

## Step 2: Test Login Flow

1. **Open browser** to: `http://localhost:5174/patient/login`

2. **Open Developer Tools** (F12 or Right-click → Inspect)

3. **Go to Console tab**

4. **Enter login credentials:**
   - Email: (the exact email from Step 1)
   - Password: anything (we don't check it)

5. **Click "Access Dashboard"**

6. **Check Console for these messages:**
   - `Attempting login with email: ...`
   - `CSRF Token: ...`
   - `Login response status: ...`
   - `[AuthContext] Starting login for: ...`

---

## Step 3: Check What's Failing

### If you see "CSRF Token: null" or no CSRF token:
**Problem:** Django isn't sending CSRF cookies
**Solution:** Check Django CORS settings

### If you see "Login response status: 302":
**Problem:** Django is redirecting (normal behavior)
**Solution:** This is actually good! Continue to next check

### If you see "Login response status: 404":
**Problem:** Django endpoint not found
**Check:** Is Django running on port 8000?

### If you see "Login response status: 500":
**Problem:** Django server error
**Check:** Django terminal for error messages

### If you see successful login but then fails:
**Problem:** Session not persisting
**Check:** Browser cookies

---

## Step 4: Quick Test Without React

Test Django login directly:

1. Go to: `http://localhost:8000/login/`
2. You should see a Django login form
3. Enter your email
4. Click submit
5. Should redirect to patient dashboard

If this works, then Django is fine and the issue is in React.

---

## What to tell me:

1. **Email address** you used when adding the patient
2. **Console output** when you try to log in
3. **Django terminal output** when you try to log in
4. **Whether Step 4** (direct Django login) works
