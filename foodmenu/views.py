from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from order.forms import CartAddProductForm
from tag.models import TaggedItem
from .forms import CategoryCreateForm, FoodCreateForm
from utils import json_menu_generator, staff_or_superuser_required, StaffSuperuserRequiredMixin, CSVExportMixin
from .models import Food, Category
from django.db.models.deletion import ProtectedError


class ListFoodView(View):
    template_name = 'menu.html'
    login_url = 'users:login'

    def get(self, request):

        menu_data = json_menu_generator()
        cart_prodict_form = CartAddProductForm()
        return render(request, self.template_name, {'menu_data': menu_data,'cart_prodict_form':cart_prodict_form})


class CreateCategoryView(View):
    template_name = 'Food_CreateCategoryTemplate.html'

    @staff_or_superuser_required
    def get(self, request):
        form = CategoryCreateForm()
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request):
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('foods:list-food')


        return render(request, 'category_form.html', {'form': form})


class CreateFoodView(View):
    template_name = 'Food_CreateFoodTemplate.html'

    def get(self, request):
        form = FoodCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FoodCreateForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save()
            print("Food Image URL:", food.foodimage.url)
            tags = form.cleaned_data.get('tags')
            for tag in tags:
                TaggedItem.objects.create(tag=tag, content_object=food)

            messages.success(request, 'Food created successfully!')
            return redirect('foods:list-food')

        return render(request, self.template_name, {'form': form})


class UpdateFoodView(View):
    template_name = 'Food_CreateFoodTemplate.html'

    @staff_or_superuser_required
    def get(self, request, pk):
        food_object = Food.objects.get(pk=pk)
        form = FoodCreateForm(instance=food_object)
        associated_tags = TaggedItem.objects.get_tags_for(Food, food_object.id).values_list('tag', flat=True)
        form.fields['tags'].initial = associated_tags
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request, pk):
        food_object = Food.objects.get(pk=pk)
        form = FoodCreateForm(request.POST, request.FILES, instance=food_object)
        if form.is_valid():
            food = form.save()
            TaggedItem.objects.filter(
                content_type=ContentType.objects.get_for_model(Food)
                , object_id=food.id).delete()
            tags = form.cleaned_data.get('tags')
            for tag in tags:
                TaggedItem.objects.create(tag=tag, content_object=food)

            messages.success(request, 'Food updated successfully!')
            return redirect('foods:list-food')

        return render(request, self.template_name, {'form': form})


class UpdateCategoryView(View):
    template_name = 'Food_CreateCategoryTemplate.html'

    @staff_or_superuser_required
    def get(self, request, pk):
        category_object = Category.objects.get(pk=pk)
        form = CategoryCreateForm(instance=category_object)
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request, pk):
        category_object = Category.objects.get(pk=pk)
        form = CategoryCreateForm(request.POST, instance=category_object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('foods:list-food')

        return render(request, 'category_form.html', {'form': form})


class DeleteCategoryView(View):
    @staff_or_superuser_required
    def get(self, request, pk):
        try:
            category_object = Category.objects.get(pk=pk)
            category_object.delete()
            messages.success(request, 'Category deleted successfully!')
            return redirect('foods:list-food')
        except Category.DoesNotExist:
            messages.error(request, 'Category does not exist!')
            return redirect('foods:list-food')



class DeleteFoodView(View):
    @staff_or_superuser_required
    def get(self, request, pk):
        try:
            food_object = Food.objects.get(pk=pk)
            food_object.delete()
            messages.success(request, 'Food deleted successfully!')
            return redirect('foods:list-food')
        except Food.DoesNotExist:
            messages.error(request, 'Food does not exist!')
            return redirect('foods:list-food')


def get_food_items(request):
    category_id = request.GET.get('category')
    if category_id :
        food_items = Food.objects.filter(category_id=category_id)

        food_list = [{'id': food.id, 'name': food.name} for food in food_items]
        return JsonResponse({'food_items': food_list})
    return JsonResponse({'food_items': None})


class AllListView(CSVExportMixin,StaffSuperuserRequiredMixin,ListView ):
    model = Food
    template_name = 'Food_ListUnTemplate.html'
    context_object_name = 'foods'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        return Food.objects.all().select_related('category')

    def get_csv_export_queryset(self):
        return self.get_queryset()

    def get_csv_export_filename(self):
        return 'foods_export'

class UnListView(AllListView):
    def get_queryset(self):
        return Food.objects.filter(availability=False).select_related('category')

class CategoryFoodsListView(AllListView):
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        return Food.objects.filter(category=category).select_related('category')

class CategoryAllView(StaffSuperuserRequiredMixin,ListView):
    model = Category
    template_name = 'Food_CategoryListTemplate.html'
    context_object_name = 'categories'
    ordering = ['-created_at']
    paginate_by = 10
    def get_queryset(self):
        return Category.objects.all().prefetch_related('parent')