from django.db import models

class Category(models.Model):
  name = models.CharField(max_length=100)
  sequence = models.IntegerField(null=True, blank=True)

  class Meta:
    verbose_name = "Category"
    verbose_name_plural = "Categories"

  def __str__(self):
    return self.name

class SubCategory(models.Model):
  category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  sequence = models.IntegerField(null=True, blank=True)

  class Meta:
    verbose_name = "Subcategory"
    verbose_name_plural = "Subcategories"

  def __str__(self):
    return f"{self.category.name} - {self.name}"
