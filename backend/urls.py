from django.urls import path
from user_api import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
	path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),
	path('products', views.ProductListCreateAPIView.as_view(), name='product-list'),
	path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product'),
	path('categories', views.CategoryList.as_view(), name='category-list'),
	path('orders', views.OrderListCreateAPIView.as_view(), name='order-list'),
	path('cart', views.CartView.as_view(), name='cart'),
]	
