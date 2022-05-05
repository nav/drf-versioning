from django.contrib import admin
from catalogue import models


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Product, ProductAdmin)
