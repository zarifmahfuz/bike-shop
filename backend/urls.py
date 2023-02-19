from django.urls import path
from . import views

urlpatterns = [
    path('bikes/', views.BikesView.as_view()),
    path('bikes/<int:id>/', views.BikeView.as_view()),
    path('customers/', views.CustomersView.as_view()),
    path('customers/<int:id>/', views.CustomerView.as_view()),
    path('sales/', views.SalesView.as_view()),
    path('sales/<int:id>/', views.SaleView.as_view()),
]
