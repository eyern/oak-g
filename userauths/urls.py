from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [

	# User Auths
	path("sing-up/", views.register_view, name="sing-up"),
	path("sing-in/", views.login_view, name="sing-in"),
	path("sing-out/", views.logout_view, name="sing-out"),

	# User Account
	path("account/", views.account, name="account"),
    
	#orders
    path('orders/', views.orders, name='orders'),
    
    path('add-address/', views.AddressView.as_view(), name="add-address"),
    
    path('remove-address/<int:id>/', views.remove_address, name="remove-address"),
]