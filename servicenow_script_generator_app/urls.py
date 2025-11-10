"""servicenow_script_generator_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path("view/", views.view_cat_subcat, name="view_cat_subcat"),

    # Category CRUD
    path("category/<int:pk>/edit/", views.edit_category, name="edit_category"),
    path("category/<int:pk>/delete/", views.delete_category, name="delete_category"),

    # SubCategory CRUD
    path("subcategory/<int:pk>/edit/", views.edit_subcategory, name="edit_subcategory"),
    path("subcategory/<int:pk>/delete/", views.delete_subcategory, name="delete_subcategory"),

    # Add to ServiceNOW tables
    path("add_to_snow/", views.add_to_snow, name="add_to_snow"),

    # Generate SNOW scripts page
    path("generate_scripts_page/", views.generate_scripts_page, name="generate_scripts_page"),

    # Handle csv uploads
    path("upload_category_csv/", views.upload_category_csv, name="upload_category_csv"),
    path("upload_subcategory_csv/", views.upload_subcategory_csv, name="upload_subcategory_csv"),

    # Generate actual SNOW scripts
    path("generate_scripts/", views.generate_scripts, name="generate_scripts"),
]
