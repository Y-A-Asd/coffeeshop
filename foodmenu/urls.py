from django.urls import path, include
from . import views

app_name = 'foods'
urlpatterns = [
    path('list-food', views.ListFoodView.as_view(), name='list-food'),
    path('create-food', views.CreateFoodView.as_view(), name='create-food'),
    path('update-food/<int:pk>', views.UpdateFoodView.as_view(), name='update-food'),
    path('update-category/<int:pk>', views.UpdateCategoryView.as_view(), name='update-category'),
    path('delete-food/<int:pk>', views.DeleteFoodView.as_view(), name='delete-food'),
    path('delete-category/<int:pk>', views.DeleteCategoryView.as_view(), name='delete-category'),
    path('create-category', views.CreateCategoryView.as_view(), name='create-category'),
    path('get_food_items/', views.get_food_items, name='get_food_items'),
    path('list-all-food/', views.AllListView.as_view(), name='list-all-food'),
    path('list-all-food/<int:category_id>', views.CategoryFoodsListView.as_view(), name='list-category-food'),
    path('list-all-food-un/', views.UnListView.as_view(), name='list-all-food-un'),
    path('list-category/', views.CategoryAllView.as_view(), name='list-category'),
    path('manage-reviews/', views.ManageReviewsView.as_view(), name='manage-reviews'),
    path('submit-review/<int:id>', views.SubmitReviewView.as_view(), name='submit-review'),
    path('approve-review/<int:id>', views.ApproveReviewView.as_view(), name='approve-review'),
    path('food-review/<int:id>', views.ListReviewsView.as_view(), name='food-review'),

]
