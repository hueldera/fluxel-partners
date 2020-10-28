from django import forms
from . import models
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _
from datetime import datetime
# class DateInput(forms.DateTimeInput):
#     input_type = 'datetime-local'


class OrderForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label=_('Briefing'))

    def clean(self):
        super().clean()

        deadline = self.cleaned_data.get('deadline')
        print(deadline)
        print(type(deadline))

        if datetime.now().date() >= deadline.date():
            self._errors['deadline'] = self.error_class(
                [_("The deadline couldn't be in past.")])
        return self.cleaned_data

    class Meta:
        model = models.Order
        fields = ['item',
                  'budget', 'customer', 'deadline', 'description']
        widgets = {
            'deadline': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})
        }

        labels = {
            'item': _('Item'),
            'budget': _('Budget'),
            'customer': _('Customer'),
            'deadline': _('Deadline'),
            'description': _('Briefing')
        }
