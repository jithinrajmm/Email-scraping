from django.contrib import admin
from extract.models import EmailData

models = [EmailData]
admin.site.register(models)

# Register your models here.
