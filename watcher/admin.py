from django.contrib import admin
from .models import watcher_model

# Register your models here.
admin.site.register(watcher_model, admin.ModelAdmin)