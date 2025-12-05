# ServiceNOW Generator App

**Deployment Link:** [https://snow-generator-app.onrender.com/](https://snow-generator-app.onrender.com/)

**NOTE: This is deployed on the free version, so sometimes it won't work due to the database expiring and me not having time to set up a new one yet.**

---

## 📌 Overview

ServiceNOW Generator App is a tool used for generating ServiceNow category and subcategory scripts in the help desk ticket form that allows users to filter categories based on subcategories and vice versa.

<img width="890" height="657" alt="readme-pic" src="https://github.com/user-attachments/assets/95621fdc-f5e7-44d6-bfb6-9748f98287ac" />


---

## 🛠️ Tech Stack

* **Framework:** Django
* **Database:** PostgreSQL
* **Hosting:** Render
* **Extras:** OpenPyXL, Django-Environ, dj-database-url

---

## 🚀 Features

* Upload categories and subcategories via CSV
* Generate Excel files from your database
* Deduplicate and sanitize category inputs
* View, edit, and delete categories/subcategories
* Uses PostgreSQL for reliable cloud storage

---

## 📂 Project Structure

```
config/
  settings.py
  urls.py
  wsgi.py

servicenow_script_generator_app/
  models.py
  views.py
  urls.py
  templates/
  static/

Procfile
requirements.txt
```

---

## 🧰 Local Setup

1. Clone the repo
2. Create a virtual environment
3. Install dependencies
4. Create a `.env` file with:

```
SECRET_KEY=<your_secret_key>
DEBUG=True
ALLOWED_HOSTS=<urls_you_allow>
DATABASE_URL=postgres://<user>:<pass>@<host>:<port>/<dbname>
```

5. Run migrations:

```
python manage.py migrate
```

6. Start server:

```
python manage.py runserver
```

---

## 🚢 Deployment (Render)

* Create a Web Service linked to your GitHub repo
* Add a Render PostgreSQL instance
* Add Environment Variables:

  * `SECRET_KEY`
  * `DEBUG=False`
  * `ALLOWED_HOSTS`
  * `DATABASE_URL`

* Use the following start command:

```
gunicorn config.wsgi
```

---
