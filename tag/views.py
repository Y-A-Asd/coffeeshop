from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import TagCreateForm
from .models import Tag
from utils import staff_or_superuser_required, StaffSuperuserRequiredMixin, CSVExportMixin


class TagListView(CSVExportMixin, StaffSuperuserRequiredMixin, ListView):
    model = Tag
    template_name = 'Tag_ListTemplate.html'
    context_object_name = 'tags'
    paginate_by = 10

    def get_csv_export_queryset(self):
        return Tag.objects.all().order_by('-label')


class TagSearchedListView(CSVExportMixin, StaffSuperuserRequiredMixin, ListView):
    model = Tag
    template_name = 'Tag_ListTemplate.html'
    context_object_name = 'tags'
    paginate_by = 10

    def get_queryset(self):
        label = self.request.GET.get('label')

        # Check if label is None before using it in the queryset
        if label is not None:
            return Tag.objects.filter(label__icontains=label)
        else:
            # Return an empty queryset or the default queryset as needed
            return Tag.objects.none()  # or Tag.objects.all() if you want to show all tags

    def get_csv_export_queryset(self):
        label = self.request.GET.get('label')

        # Check if label is None before using it in the queryset
        if label is not None:
            return Tag.objects.filter(label__icontains=label).order_by('-label')
        else:
            return Tag.objects.none()


class CreateTagView(StaffSuperuserRequiredMixin, CreateView):
    model = Tag
    template_name = 'Tag_CreateTemplate.html'
    form_class = TagCreateForm
    success_url = reverse_lazy('tags:tag')


class DeleteTagView(View):
    @staff_or_superuser_required
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
        return redirect('tags:tag')


class TagChangeAvailabilityView(View):
    @staff_or_superuser_required
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        if tag.label == "unavailable":
            messages.error(request, 'You can not change this tag availability!')
            return redirect('tags:tag')
        tag.available = not tag.available
        tag.save()
        messages.success(request, 'Tag Changed successfully!')
        return redirect('tags:tag')
