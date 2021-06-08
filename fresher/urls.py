from django.urls import path

from . import views

app_name = 'fresher'

urlpatterns = [
    path('', views.recipe_all, name='fresher_home'),
    path('<slug:slug>', views.recipe_detail, name='recipe_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
]
