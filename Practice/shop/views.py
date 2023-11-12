from django.shortcuts import render

# Create your views here.
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import*
from django.urls import reverse
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category, Basket, Order, OrderItem
from django.db.models import Q
from django.core.paginator import Paginator, Page
from .serializers import ProductSerializer, CategorySerializer, BasketSerializer
from django.views.generic import TemplateView, ListView
from rest_framework.response import Response
from django.shortcuts import render, redirect, HttpResponseRedirect


class LoginUserView(LoginView):
    form_class = AccountLoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_user_context(self, **kwargs):
        context = kwargs

        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")

        return dict(list(context.items()) + list(c_def.items()))




def register(request):
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')  # Замените 'home' на URL вашей главной страницы
    else:
        form = AccountRegisterForm()
    return render(request, 'registration/registration.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class ProductsListAPIView(ListAPIView):
    '''
    Вывод товаров для мужчин и женщин
    '''
    serializer_class = ProductSerializer
    template_name = 'shop/catalog.html'

    def get_queryset(self):
        queryset = Product.objects.all()

        # Получаем параметры фильтрации из запроса
        type = self.request.GET.get('type')
        categories = self.request.GET.getlist('category')

        # Применяем фильтры
        if type:
            queryset = queryset.filter(type=type)


        if categories:
            category_filters = Q()
            for category in categories:
                category_filters |=Q(category=category)
            queryset = queryset.filter(category_filters)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().all()
        product_serializer = self.get_serializer(queryset, many=True)


        # brands = Manufacturer.objects.values()
        categories = Category.objects.values()

        # Добавьте пагинацию к вашему queryset
        page_number = request.GET.get('page')
        paginator = Paginator(product_serializer.data, 6)  # 10 товаров на странице
        page = paginator.get_page(page_number)

        return render(request,
                      self.template_name,
                      {'products': page,
                       # 'brands': brands,
                       'categories': categories
                       }
                      )

class Search(ListView):

    template_name = 'shop/search.html'


    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context

def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(current_page)


def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketListAPIView(ListAPIView):
    serializer_class = BasketSerializer
    template_name = 'shop/cart.html'

    def get_queryset(self):
        queryset = Basket.objects.filter(user=self.request.user)
        return queryset

    def get_total_quantity(self):
        baskets = self.get_queryset()
        return sum(basket.quantity for basket in baskets)

    def get_total_sum(self):
        baskets = self.get_queryset()
        return sum(basket.sum() for basket in baskets)

    def get(self, request, *args, **kwargs):
        context = {
            'baskets': self.get_queryset(),
            'total_quantity': self.get_total_quantity(),
            'total_sum': self.get_total_sum(),
            }
        return render(request, self.template_name, context)

# def abc(request):
#     return render(request, 'shop/index.html')

class MainPage(ListAPIView):
    template_name = 'shop/index.html'

    def get_queryset(self):
        queryset = Product.objects.filter(is_new=True)
        return queryset

    def get(self, request, *args, **kwargs):
        context = {
            'products': self.get_queryset()
        }

        return render(request, self.template_name, context)

class ProductAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    template_name = 'shop/product.html'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        context = {'product': instance}

        return render(request, self.template_name, context)


def create_order(request):
    # Получаем текущего пользователя
    user = request.user

    # Получаем товары из корзины пользователя
    basket_items = Basket.objects.filter(user=user)

    if basket_items.exists():
        # Создаем новый заказ
        order = Order.objects.create(user=user,)

        # Создаем объекты OrderItem на основе содержимого корзины
        for basket_item in basket_items:
            order_item = OrderItem.objects.create(
                product=basket_item.product,
                quantity=basket_item.quantity,
                price=basket_item.product.price * basket_item.quantity
            )
            order.items.add(order_item)

        # Очищаем корзину, но не удаляем объекты
        basket_items.delete()

        return redirect('order-success')  # Перенаправляем пользователя на страницу успешного оформления заказа


def order_success(request):
    return render(request, 'shop/order.html')

def about_us(request):
    return render(request, 'shop/about_us.html')