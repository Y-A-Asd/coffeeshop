from datetime import datetime

from django.shortcuts import render
from django.views import View
from utils import Reporting, staff_or_superuser_required
from decimal import Decimal


# Create your views here.
class HomeView(View):
    template_name = 'Core_HomeTemplate.html'

    def get(self, request):
        try:
            context = {'name': request.user.phone_number}
        except Exception:
            context = {'name': None}
        return render(request, self.template_name, context)


class DashboardView(View):
    template_name = 'Core_DashboardTemplate.html'

    @staff_or_superuser_required
    def get(self, request):

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')


        selected_range = request.GET.get('range', 'month')

        if selected_range == 'year':
            days = 365
        elif selected_range == 'week':
            days = 7
        elif selected_range == 'day':
            days = 1
        elif selected_range == 'month':
            days = 30
        elif selected_range == 'total':
            days = 99999

        reporting_params = {'days': days}

        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date, '%m/%d/%Y').date()
            end_date_obj = datetime.strptime(end_date, '%m/%d/%Y').date()
            reporting_params = {'start_at': start_date_obj, 'end_at': end_date_obj}

        r = Reporting(reporting_params)

        total_sales: Decimal = r.total_sales()
        percentage_difference = r.get_percentage_difference()
        peak_hour, most_peak_hour = r.peak_hours()
        context = {
            'total_sales': total_sales,
            'percentage_difference': percentage_difference,
            'favorite_food': r.favorite_foods(),
            'favorite_table': r.favorite_tables(),
            'peak_hour': peak_hour,
            'peak_day': r.peak_day_of_week(),
            'most_peak_hour': most_peak_hour,
            'best_cutomer': r.best_cutomer(),
            'favorite_category': r.favorite_category(),
            'sales_by_employee': r.sales_by_employee(),
            'order_status_counts': r.order_status_counts(),
        }

        return render(request, self.template_name, context=context)

def document(request):
    return render(request, '_build/html/index.html')
def about_us(request):
  return render(request, 'templates/pages/about-us.html')