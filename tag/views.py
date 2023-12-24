from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView

from .models import Tag


class TagListView(ListView):
    model = Tag
    template_name = 'Tag_ListTemplate.html'
    context_object_name = 'tags'

class CreateTagView(CreateView):
    model = Tag
    template_name = 'Tag_CreateTemplate.html'
    fields = ['label', 'available']
    success_url = reverse_lazy('tags:tag')

class DeleteTagView(View):
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        return redirect('tags:tag')

class TagChangeAvailabilityView(View):
    def post(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.available = not tag.available
        tag.save()
        return redirect('tags:tag')



