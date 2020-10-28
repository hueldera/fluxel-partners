from modeltranslation.translator import translator, TranslationOptions
from .models import Status


class StatusTranslationOptions(TranslationOptions):
    fields = ('name',)


# translator.register(Status, StatusTranslationOptions)
