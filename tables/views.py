from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import NoReverseMatch, reverse_lazy
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from order.models import Order
from utils import staff_or_superuser_required, StaffSuperuserRequiredMixin
from .forms import Reservation as ReservationForm
from .forms import ReservationGetForm, CreateTableForm
from .models import Reservation as ReservationModel
from .models import Table
from django.views.generic import ListView, DeleteView


class CreateReservationView(View):
    template_name = 'Reservation_CreateTemplate.html'

    def get(self, request):
        form = ReservationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            datetime = form.cleaned_data['datetime']
            number_of_persons = form.cleaned_data['number_of_persons']
            reservation = ReservationModel(phone_number=phone_number,
                                           datetime=datetime,
                                           number_of_persons=number_of_persons)
            reservation.save()
            messages.success(request,
                             'Reservation created successfully.')
            return redirect('core:home')
        else:
            return render(request, self.template_name, {'form': form})


class ListReservationView(LoginRequiredMixin, View):
    template_name = 'Reservation_ListTemplate.html'
    paginate_by = 10

    @staff_or_superuser_required
    def get(self, request):
        reservation_list = ReservationModel.objects.all().order_by('-created_at')
        tables = Table.objects.all()

        # Using Django's built-in ListView for pagination
        paginator = Paginator(reservation_list, self.paginate_by)
        page = request.GET.get('page')

        try:
            reservation_list = paginator.page(page)
        except PageNotAnInteger:
            reservation_list = paginator.page(1)
        except EmptyPage:
            reservation_list = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'reservation_list': reservation_list, 'tables': tables})

    @staff_or_superuser_required
    def post(self, request):
        reservation_id = request.POST.get('reservation_id')
        action = request.POST.get('action')

        try:
            reservation = ReservationModel.objects.get(id=reservation_id)

            if action == 'set':
                table_id = request.POST.get('table_id')
                if table_id == 'Null':
                    reservation.table = None
                    reservation.save()
                else:
                    table = Table.objects.get(id=table_id)
                    reservation.table = table
                    reservation.save()
                messages.success(request, 'Table set successfully.')

                new_status = request.POST.get('new_status')
                reservation.status = new_status
                reservation.save()
                messages.success(request, 'Status updated successfully.')
            return redirect('tables:list-reservation')

        except ReservationModel.DoesNotExist:
            messages.error(request, 'Reservation does not exist.')
            return redirect('tables:list-reservation')


class DetailReservationView(View):
    template_name = 'Reservation_DetailTemplate.html'

    @staff_or_superuser_required
    def get(self, request, pk):
        tables = Table.objects.all()
        try:
            reservation = ReservationModel.objects.get(pk=pk)
            pk = reservation.pk
            phone_number = reservation.phone_number
            datetime = reservation.datetime
            number_of_persons = reservation.number_of_persons
            table = reservation.table
            status = reservation.status
            context = {'id': id, 'phone_number': phone_number, 'datetime': datetime,
                       'number_of_persons': number_of_persons,
                       'table': table, 'status': status,
                       'tables': tables, 'pk': pk}
        except ReservationModel.DoesNotExist:
            messages.error(request,
                           'Reservation does not exist.')
            return redirect('tables:list-reservation')
        return render(request, self.template_name, context=context)

    @staff_or_superuser_required
    def post(self, request, pk):
        reservation_id = request.POST.get('reservation_id')
        action = request.POST.get('action')

        try:
            reservation = ReservationModel.objects.get(id=reservation_id)

            if action == 'set':
                table_id = request.POST.get('table_id')
                if table_id == 'Null':
                    reservation.table = None
                    reservation.save()
                else:
                    table = Table.objects.get(id=table_id)
                    reservation.table = table
                    reservation.save()
                messages.success(request, 'Table set successfully.')
                new_status = request.POST.get('new_status')
                reservation.status = new_status
                reservation.save()
                messages.success(request, 'Status updated successfully.')
            return redirect('tables:detail-reservation', pk)

        except ReservationModel.DoesNotExist:
            messages.error(request, 'Reservation does not exist.')
            return redirect('tables:list-reservation')


class GetReservationView(View):
    template_name = 'Reservation_GetTemplate.html'

    @staff_or_superuser_required
    def get(self, request):
        form = ReservationGetForm()
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request):
        form = ReservationGetForm(request.POST)
        try:
            if form.is_valid():
                return redirect('tables:detail-reservation', form.cleaned_data['code'])
            else:
                messages.error(request,
                               'Reservation does not exist.')
                return render(request, self.template_name, {'form': form})
        except NoReverseMatch:
            messages.error(request,
                           'Invalid code')
            return render(request, self.template_name, {'form': form})


class CreateTableView(View):
    template_name = 'Reservation_CreateTable.html'

    @staff_or_superuser_required
    def get(self, request):
        form = CreateTableForm()
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request):
        form = CreateTableForm(request.POST)
        if form.is_valid():
            Table.objects.all().delete()
            for i in range(1, form.cleaned_data['number'] + 1):
                Table.objects.create(number=i)
            messages.success(request,
                             'Tables created successfully')

            redirect('tables:list-table')


# @staff_or_superuser_required

class ListTableView(StaffSuperuserRequiredMixin, ListView):
    model = Table
    template_name = 'Reservation_ListTableTemplate.html'
    context_object_name = 'table'

    def get_queryset(self):
        return Table.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['table_orders'] = {}
        # for table_instance in context['table']:
        #     try:
        #         order = Order.objects.filter(table=table_instance, status__in=["W", "P", "T"])
        #         context['table_orders'][table_instance.id] = order
        #     except Order.DoesNotExist:
        #         pass

        table_ids = [table.id for table in context['table']]

        orders_dict = Order.objects.filter(
            deleted_at__isnull=True,
            status__in=["W", "P", "T"],
            table_id__in=table_ids
        ).order_by('-created_at').in_bulk(field_name='id')
        """
        
        in_bulk():
        
        Takes a list of field values (id_list) and the field_name for those values,
         and returns a dictionary mapping each value to an instance of the object with the given field value.
          No django.core.exceptions.ObjectDoesNotExist exceptions will ever be raised by in_bulk;
           that is, any id_list value not matching any instance will simply be ignored.
            If id_list isn’t provided, all objects in the queryset are returned.
             field_name must be a unique field or a distinct field (if there’s only one field specified in distinct()).
              field_name defaults to the primary key.
              
        """
        context['table_orders'] = {table.id: orders_dict.get(table.id, []) for table in context['table']}

        return context


class ChangeStatusTableView(StaffSuperuserRequiredMixin,View):

    @staff_or_superuser_required
    def post(self, request, pk, status):
        table = Table.objects.get(pk=pk)
        order = Order.objects.filter(table=table, status__in=["W", "P", "T"]).first()

        if order:
            messages.error(request, 'Table has an order you cannot cheng status')
            return redirect('tables:list-table')

        if table.status == "T":
            messages.error(request, 'you cannot cheng status of TakeAway Table')
            return redirect('tables:list-table')
        table.status = status
        table.save()
        messages.success(request, 'Table status changed successfully!')
        return redirect('tables:list-table')


class DeleteTableView(StaffSuperuserRequiredMixin, DeleteView):
    model = Table
    template_name = 'Reservation_DeleteTableTemplate.html'
    success_url = reverse_lazy('tables:list-table')
    context_object_name = 'table'

    def delete(self, request, *args, **kwargs):
        table = self.get_object()
        return super().delete(request, *args, **kwargs)
