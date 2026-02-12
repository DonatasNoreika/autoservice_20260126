from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_pk>/', views.car, name='car'),
    path('search/', views.search, name='search'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path("userorders/", views.UserOrderListView.as_view(), name="userorders"),
    path('orders/', views.OrderListView.as_view(), name="orders"),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name="order"),
    path('orders/create/', views.OrderCreateView.as_view(), name="order_create"),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name="order_update"),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name="order_delete"),
]
