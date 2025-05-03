# Vehicle Registration System

A Django-based web application for vehicle registration and management. This project allows administrators to manage vehicles and users, and allows regular users to register, log in, and interact with the system.

---

## Features
- User registration and login
- Admin dashboard to add, update, and delete vehicles
- Vehicle list with search and filtering
- User management (excluding admin user)
- Clean, responsive UI with Bootstrap

---

## Technologies Used
- Python 3
- Django 5.x
- SQLite (default DB)
- HTML/CSS/Bootstrap
- JavaScript
- [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) for form styling

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd vehicle_registartion
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv

# Windows
env\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```
If `requirements.txt` is missing:
```bash
pip install django widget-tweaks
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
admin: rahul
password: rahul@2005
```
Follow prompts to set up an admin user.

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Admin Panel Access
Visit: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and log in using the superuser credentials.

---

## File Structure
```
vehicle_registartion/
├── manage.py
├── project_name/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── vehicles/
│   ├── templates/vehicles/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── forms.py
└── static/
```

---

## Notes
- Make sure `widget_tweaks` is in your `INSTALLED_APPS`.
- Static files may require `python manage.py collectstatic` for deployment.
- To exclude the admin user from listings, filter by `is_superuser=False` in your views.

---

## License
This project is licensed for educational and non-commercial use.

---

## Author
Your Name - [rahulmalu111@gmail.com]
