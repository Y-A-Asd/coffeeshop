from django.contrib import admin

# Register your models here.
from .models import Offkey


# @admin.register(Offkey)
# class CouponAdmin(admin.ModelAdmin):
#     list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active', 'mode']
#     list_filter = ['active', 'valid_from', 'valid_to']
#     search_fields = ['code']



from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms

class OffkeyAdminForm(forms.ModelForm):
    class Meta:
        model = Offkey
        fields = ['code', 'valid_from', 'valid_to', 'discount', 'active', 'mode']

    def clean(self):
        """
            https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
            https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/#overriding-clean-on-a-modelformset
            https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/#overriding-methods-on-an-inlineformset
        """
        cleaned_data = super().clean()
        mode = cleaned_data.get('mode')
        valid_to = cleaned_data.get('valid_to')

        if mode == Offkey.Mode.OneTime and valid_to is not None:
            raise ValidationError({'valid_to': 'Valid To should be blank for OneTime mode.'})

        if mode == Offkey.Mode.TimeEvent and valid_to is None:
            raise ValidationError({'valid_to': 'Valid To is required for TimeEvent mode.'})

        return cleaned_data


class OffkeyAdmin(admin.ModelAdmin):
    form = OffkeyAdminForm

admin.site.register(Offkey, OffkeyAdmin)