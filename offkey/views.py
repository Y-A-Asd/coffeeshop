from django.contrib import messages
from django.utils import timezone
from .forms import GetOff
from django.shortcuts import render, redirect
from django.views import View
from .models import Offkey

# Create your views here.


class OffKeyView(View):
    """
    https://stackoverflow.com/questions/62359009/django-how-to-reduce-total-number-of-coupons-after-each-use
    """
    def post(self, request, *args, **kwargs):
        now = timezone.now()
        form = GetOff(request.POST)
        response = redirect('order:detail-cart')
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                offkey = Offkey.objects.get(code=code,
                                            valid_from__lte=now,
                                            active=True
                                            )
                if offkey.mode == 'OT':
                    # offkey.active = False
                    # offkey.save()
                    pass
                else:
                    if not offkey.valid_to >= now:
                        raise Offkey.DoesNotExist()
                messages.success(request, 'Code applied successfully')
                response.set_cookie('offkey', offkey.id)
            except Offkey.DoesNotExist:
                messages.error(request, "Code doesn't found")
                response.set_cookie('offkey', None)

        return response
