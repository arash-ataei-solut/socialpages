from django.contrib import admin

from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover',)
    sortable_by = ('title',)


admin.site.register(models.Post, ProductAdmin)
admin.site.register(models.MediaFile)
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.Rate)
