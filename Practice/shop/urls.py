from django.urls import path
from .views import *

urlpatterns = [
    #path('account/<int:pk>/', StoreUserAPIView.as_view(), name='user-detail'),
    # path('login', StoreUserLoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('register', register, name = 'register'),
    path('', MainPage.as_view(), name='main'),
    path('catalog', ProductsListAPIView.as_view(), name= 'catalog'),
    path('search', Search.as_view(), name='search'),
    path('my-cart', BasketListAPIView.as_view(), name='cart'),
    path('basket-add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket-delete/<int:id>/', basket_delete, name='basket_delete'),
    path('product/<int:pk>/', ProductAPIView.as_view(), name='product'),
    path('order-success',order_success, name='order-success'),
    path('create-order', create_order, name='create_order'),
    path('about_us/', about_us, name='about_us'),
]