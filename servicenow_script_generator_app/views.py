from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, SubCategory
from django.contrib import messages
from collections import defaultdict
from django.http import JsonResponse
import json, csv

def home(request):
  if request.method == "POST":
    # Clear out old categories and subcategories
    Category.objects.all().delete()
    SubCategory.objects.all().delete()

    # Add all combos (JSON payload from hidden input)
    all_combos_json = request.POST.get("all_combos")
    if all_combos_json:
      try:
        all_combos = json.loads(all_combos_json)
        
        # Step 1: Build a unique mapping of category -> unique subcategories
        category_map = {}
        for combo in all_combos:
          category_name = combo.get("category", "").strip()
          subcategories = [s.strip() for s in combo.get("subcategories", []) if s.strip()]
          if not category_name:
              continue
          if category_name not in category_map:
            category_map[category_name] = set()
          category_map[category_name].update(subcategories)

        # Step 2: Insert cleaned data into DB
        for category_name, subcats in category_map.items():
          category = Category.objects.create(name=category_name)
          for sub in sorted(subcats):  # sorted() optional, just for consistency
            SubCategory.objects.create(category=category, name=sub)

      except json.JSONDecodeError:
        # Might want to log or handle malformed JSON here
        pass

    # Redirect to add_to_snow page after processing
      return redirect("add_to_snow")

  # GET request – just render everything
  categories = Category.objects.prefetch_related("subcategories").all()
  return render(request, "home.html", {"categories": categories})

def view_cat_subcat(request):
  # GET request – just render everything
  categories = Category.objects.prefetch_related("subcategories").all()
  subcategories = SubCategory.objects.select_related("category").all()

  # Category search
  category_search = request.GET.get("category_search", "").strip()
  if category_search:
    categories = categories.filter(name__icontains=category_search)

  # Subcategory search
  sub_search = request.GET.get("subcategory_search", "").strip()
  # default: subcategory
  search_by = request.GET.get("search_by", "subcategory")

  if sub_search:
    if search_by == "category":
      subcategories = subcategories.filter(category__name__icontains=sub_search)
    # search by subcategory name
    else:  
      subcategories = subcategories.filter(name__icontains=sub_search)

  return render(request, "view_cat_subcat.html", {
    "categories": categories,
    "subcategories": subcategories,
    "category_count": categories.count(),
    "subcategory_count": subcategories.count(),
  })

# CRUD: Category
def edit_category(request, pk):
  category = get_object_or_404(Category, pk=pk)
  if request.method == "POST":
    new_name = request.POST.get("name", "").strip()
    if new_name:
      category.name = new_name
      category.save()
      return redirect("view_cat_subcat")
  return render(request, "edit.html", {
    "object": category,
    "type": "Category"
  })

def delete_category(request, pk):
  category = get_object_or_404(Category, pk=pk)
  subcategories_count = category.subcategories.count()

  if request.method == "POST":
    if subcategories_count == 0:
      category.delete()
      messages.success(request, f"Category '{category.name}' deleted successfully.")
      return redirect("view_cat_subcat")
    # Cannot delete category if it has subcategories
    else: 
      messages.error(request, f"Cannot delete category '{category.name}' because it has {subcategories_count} associated subcategories.")
      return redirect("view_cat_subcat")

  return render(request, "confirm_delete.html", {
    "object": category,
    "type": "Category",
    "cancel_url": "view_cat_subcat",
    "subcategories_count": subcategories_count
  })

# CRUD: SubCategory
def edit_subcategory(request, pk):
  sub = get_object_or_404(SubCategory, pk=pk)
  if request.method == "POST":
    new_name = request.POST.get("name", "").strip()
    if new_name:
      sub.name = new_name
      sub.save()
      return redirect("view_cat_subcat")
  return render(request, "edit.html", {
    "object": sub,
    "type": "Subcategory"
  })

def delete_subcategory(request, pk):
  sub = get_object_or_404(SubCategory, pk=pk)
  if request.method == "POST":
    sub.delete()
    return redirect("view_cat_subcat")
  return render(request, "confirm_delete.html", {
    "object": sub,
    "type": "Subcategory",
    "cancel_url": "view_cat_subcat"
  })

def add_to_snow(request):
  categories = Category.objects.all()
  subcategories = SubCategory.objects.select_related("category").all()
  return render(request, "add_to_snow.html", {
    "categories": categories,
    "subcategories": subcategories
  })

def generate_scripts_page(request):
  return render(request, "generate_scripts.html")

def upload_category_csv(request):
  upload_message = None
  categories = Category.objects.all()

  if request.method == "POST" and request.FILES.get("category_csv_file"):
    csv_file = request.FILES["category_csv_file"]

    if not csv_file.name.endswith('.csv'):
      upload_message = "❌ Please upload a valid CSV file."
    else:
      # Read and decode the file
      decoded_file = csv_file.read().decode("utf-8").splitlines()
      reader = csv.DictReader(decoded_file)

      # Clear old categories
      Category.objects.all().delete()

      # Insert fresh categories from "value" column
      categories_to_create = []
      for row in reader:
        value = row.get("value")
        inactive = row.get("inactive").lower()

        # skip blank and inactive rows 
        if value and inactive == "false":  
          categories_to_create.append(Category(name=value))

      Category.objects.bulk_create(categories_to_create)
      upload_message = f"✅ Successfully uploaded {len(categories_to_create)} categories from CSV."

      categories = Category.objects.all()

  return render(request, "generate_scripts.html", {
    "categories": categories,
    "upload_message": upload_message
  })

def upload_subcategory_csv(request):
  upload_message = None
  subcategories = SubCategory.objects.select_related("category").all()

  if request.method == "POST" and request.FILES.get("subcategory_csv_file"):
    csv_file = request.FILES["subcategory_csv_file"]

    if not csv_file.name.endswith('.csv'):
      upload_message = "❌ Please upload a valid CSV file."
    else:
      # Read and decode the file
      decoded_file = csv_file.read().decode("utf-8").splitlines()
      reader = csv.DictReader(decoded_file)

      # Clear old subcategories
      SubCategory.objects.all().delete()

      # Insert fresh subcategories from CSV
      subcategories_to_create = []

      # Track subcatories that are missing a valid category
      missing_categories = []

      for row in reader:
        value = row.get("value")
        inactive = row.get("inactive").lower()
        category_name = row.get("dependent_value") or "" 

        # Skip blank, inactive, or missing category rows
        if value and inactive == "false" and category_name != "":
          try:
            category = Category.objects.get(name=category_name)
            subcategories_to_create.append(
              SubCategory(category=category, name=value)
            )
          except Category.DoesNotExist:
            missing_categories.append(value)
        # Log subcategories skipped due to missing category
        elif category_name == "":
          missing_categories.append(value)

      SubCategory.objects.bulk_create(subcategories_to_create)

      # Build upload message
      success_count = len(subcategories_to_create)
      if missing_categories:
        upload_message = (
          f"✅ Uploaded {success_count} subcategories.\n"
          f"⚠️ Skipped {len(missing_categories)} subcategories because their category was missing/didn't match what was in the Category table:\n"
          + ", ".join(missing_categories)
        )
      else:
        upload_message = f"✅ Successfully uploaded {success_count} subcategories from CSV."

      subcategories = SubCategory.objects.select_related("category").all()

  return render(request, "generate_scripts.html", {
    "subcategories": subcategories,
    "upload_message_subcategories": upload_message
  })

def build_category_based_on_subcat_string(category_based_on_subcat, all_categories):
  js = []
  js.append("function onChange(isLoading) {")
  js.append("    if (isLoading) {")
  js.append("        return;")
  js.append("    }")
  js.append("")

  # Dump allCategories as JSON (safe for JS)
  js.append(f"  var allCategories = {json.dumps(all_categories)};")
  js.append("")
  js.append("  var subCat = g_form.getValue('subcategory');")
  js.append("  var category = g_form.getControl('category');")
  js.append("")
  js.append("  g_form.clearOptions('category');")
  js.append("")
  js.append("  switch (subCat) {")
  js.append('    case "":')
  js.append("      addOptions(category, allCategories);")
  js.append("      break;")
  js.append("")

  # Loop through mappings to create cases
  for sub, cats in category_based_on_subcat.items():
    if sub == '':
      continue
    case_line = f'    case "{sub}":'
    options = json.dumps([''] + cats)  
    js.append(case_line)
    js.append(f"      addOptions(category, {options});")
    js.append("      break;")
    js.append("")

  js.append("  }")
  js.append("")
  js.append("  function addOptions(element, options) {")
  js.append("    options.forEach(function(option) {")
  js.append("      var label = option === '' ? '-- None --' : option;")
  js.append("      g_form.addOption('category', option, label);")
  js.append("    });")
  js.append("  }")
  js.append("}")

  return "\n".join(js)

def build_subcategory_based_on_category_string(subcat_based_on_category, all_subcategories):
  js = []
  js.append("function onChange(isLoading) {")
  js.append("    if (isLoading) {")
  js.append("        return;")
  js.append("    }")
  js.append("")

  # Dump allCategories as JSON (safe for JS)
  js.append(f"  var allSubCategories = {json.dumps(all_subcategories)};")
  js.append("")
  js.append("  var category = g_form.getValue('category');")
  js.append("  var subCat = g_form.getControl('subcategory');")
  js.append("")
  js.append("  g_form.clearOptions('subcategory');")
  js.append("")
  js.append("  switch (category) {")
  js.append('    case "":')
  js.append("      addOptions(subCat, allSubCategories);")
  js.append("      break;")
  js.append("")

  # Loop through mappings to create cases
  for cat, subs in subcat_based_on_category.items():
    if cat == '':
      continue
    case_line = f'    case "{cat}":'
    options = json.dumps([''] + subs)  
    js.append(case_line)
    js.append(f"      addOptions(subcategory, {options});")
    js.append("      break;")
    js.append("")
    

  js.append("  }")
  js.append("")
  js.append("  function addOptions(element, options) {")
  js.append("    options.forEach(function(option) {")
  js.append("      var label = option === '' ? '-- None --' : option;")
  js.append("      g_form.addOption('subcategory', option, label);")
  js.append("    });")
  js.append("  }")
  js.append("}")

  return "\n".join(js)

def generate_scripts(request):
  categories = Category.objects.all()
  subcategories = SubCategory.objects.select_related("category").all()

  # List of all categories and subcategories 
  all_categories = [''] + [cat.name for cat in categories]
  all_subcategories = [''] + [sub.name for sub in subcategories]
  
  # Create defaultdict to hold category/subcategory mappings
  subcat_based_on_category = defaultdict(list)
  category_based_on_subcat = defaultdict(list)

  # Map subcategories to their categories and vice versa
  for sub in subcategories:
    subcat_based_on_category[sub.category.name].append(sub.name)
    category_based_on_subcat[sub.name].append(sub.category.name)

  # Build JS strings
  category_based_on_subcat_string = build_category_based_on_subcat_string(category_based_on_subcat, all_categories)
  subcat_based_on_category_string = build_subcategory_based_on_category_string(subcat_based_on_category, all_subcategories)

  return JsonResponse({
    "category_based_on_subcat_script": category_based_on_subcat_string,
    "subcat_based_on_category_script": subcat_based_on_category_string,
  })