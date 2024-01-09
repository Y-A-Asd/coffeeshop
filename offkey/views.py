from datetime import timezone
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
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                offkey = Offkey.objects.get(code=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True
                                            )
                request.session['offkey'] = offkey.id
            except Offkey.DoesNotExist:
                request.session['offkey'] = None

        return redirect('order:detail-cart')
