from django.db import models
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from django.core.validators import validate_image_file_extension
from sqlalchemy import null
from django.urls import reverse

class MyModelName(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
    # …

    # Metadata
    class Meta:
        ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.my_field_name


class Supplier(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    company_name = models.CharField(max_length=200)
    reg_number = models.CharField(max_length=13)
    full_company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    head_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    reg_date = models.DateField(max_length=50)
    company_age = models.DecimalField(max_digits=6, decimal_places=2)
    industry_type = models.CharField(max_length=254)
    summary_indicator = models.CharField(max_length=15)
    share_capital = models.DecimalField(max_digits=20, decimal_places=2)
    sale_articles = models.CharField(max_length=254)
    important_info = models.CharField(max_length=254)
    product_supplier = models.CharField(max_length=254)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author is a string rather than an object because it hasn't been declared yet in the file
    


    def __str__(self):
        """String for representing the Model object."""
        return self.title
