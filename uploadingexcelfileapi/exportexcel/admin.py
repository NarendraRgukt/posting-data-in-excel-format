from django.contrib import admin

from exportexcel import models

admin.site.register(models.User)
admin.site.register(models.Item)