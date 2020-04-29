from django.contrib import admin

from . import models


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover',)
    sortable_by = ('title',)


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.MediaFile)
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.Rate)
