# ServiceNOW Generator App

**Deployment Link:** [https://snow-generator-app.onrender.com/](https://snow-generator-app.onrender.com/)

---

## 📌 Overview

ServiceNOW Generator App is a Django-powered tool used for uploading, managing, and generating structured ServiceNow category and subcategory data.

You can include a project screenshot here:

![Project Screenshot](/Users/matthewpourroy/code/servicenow_script_generator_app/servicenow_script_generator_app/static/servicenow_script_generator/images/readme-pic.png)

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

  * `DATABASE_URL`
  * `SECRET_KEY`
  * `DEBUG=False`
* Use the following start command:

```
python manage.py migrate && gunicorn config.wsgi
```

---

## 📧 Contact

If you have feedback or want to report an issue, feel free to open a GitHub issue or reach out!