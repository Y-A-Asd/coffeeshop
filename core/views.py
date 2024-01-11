from datetime import datetime

from django.apps import apps
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from .models import AuditLog
from utils import Reporting, staff_or_superuser_required, SuperuserRequiredMixin
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

# def document(request):
#     return render(request, '_build/html/index.html')
def about_us(request):
  return render(request, 'templates/pages/about-us.html')


class LogListView(SuperuserRequiredMixin, ListView):
    model = AuditLog
    template_name = 'Core_LogList.html'
    context_object_name = 'logs'
    ordering = ['-timestamp']
    paginate_by = 15


class RetrieveChangesView(SuperuserRequiredMixin, View):
    # todo: make it revert all changes until checkpoint
    # todo: make it revert all changes until checkpoint
    # todo: make it revert all changes until checkpoint
    # todo: make it revert all changes until checkpoint
    # todo: make it revert all changes until checkpoint
    # todo: make it revert all changes until checkpoint
    # todo: make it revert all changes until checkpoint
    def post(self, request, *args, **kwargs):
        log_id = self.kwargs['log_id']
        log_entry = get_object_or_404(AuditLog, id=log_id)

        app_name, model_name = log_entry.table_name.split('_')

        # mage mishe inghadar ziba bashe ?? :-)

        model_class = apps.get_model(app_label=app_name, model_name=model_name)

        model_instance = get_object_or_404(model_class, id=log_entry.row_id)
        if log_entry.changes:
            for field_name, field_data in log_entry.changes.items():
                setattr(model_instance, field_name, field_data['old_value'])
                if model_instance.deleted_at =="None":
                    model_instance.deleted_at = None
            model_instance.save()

            AuditLog.objects.create(
                user=request.user,
                action='RETRIEVE',
                table_name=log_entry.table_name,
                row_id=log_entry.row_id,
                old_value=log_entry.old_value,
                changes=None
            )
            messages.success(request, "Changes reverted successfully.")
            return redirect('core:logs')

        else:
            messages.success(request, "No changes to revert.")
            return redirect('core:logs')