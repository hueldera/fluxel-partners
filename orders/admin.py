from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from . import models


class StatusAdmin(TranslationAdmin):
    pass


admin.site.register(models.Order)
admin.site.register(models.Status)  # StatusAdmin)
admin.site.register(models.TypeItem)
admin.site.register(models.Type)
admin.site.register(models.StatusChange)
admin.site.register(models.Message)
