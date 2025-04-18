from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendorDashboard, name = 'vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'), 
    path('menu_builder/category/<int:pk>/', views.products_by_category, name='products_by_category'),
    # category crud
    path ('menu_builder/category/add/', views.add_category, name='add_category'),
    path('menu_builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu_builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    # product crud
    path('menu_builder/product/add/', views.add_product, name='add_product'),
    path('menu_builder/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('menu_builder/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
]

