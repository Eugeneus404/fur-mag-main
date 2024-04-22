"""
Definition of views.
"""

from asyncio.windows_events import NULL
from datetime import datetime
from django.shortcuts import render, redirect, Http404
from django.http import HttpRequest, JsonResponse
from app.models import Category
from app.models import Product
from app.models import Order
from app.models import OrderProduct
from .forms import AnketaForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import json
from decimal import Decimal
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def home(request):
    """Renders the home page."""
    def build_category_tree(categories, parent_id=None, parent_path=""):
        category_tree = []
        for category in categories:
            if category.parent_id == parent_id:
                path = f"{parent_path}/{category.url}" if parent_path else category.url
                children = build_category_tree(categories, parent_id=category.id, parent_path=path)
                category_data = {
                    'id': category.id,
                    'parent': category.parent_id,
                    'name': category.name,
                    'url': category.url,
                    'path': path,
                    'children': children
                }
                category_tree.append(category_data)
        return category_tree

    categories = Category.objects.all()
    category_tree = build_category_tree(categories)
    
    products = Product.objects.filter(remain__gt=0).order_by('?')[:4]

    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'year': datetime.now().year,
            'categories': category_tree,
            'products': products,
        }
    )

def catalog(request):
    """Renders the home page."""
    def build_category_tree(categories, parent_id=None, parent_path=""):
        category_tree = []
        for category in categories:
            if category.parent_id == parent_id:
                path = f"{parent_path}/{category.url}" if parent_path else category.url
                children = build_category_tree(categories, parent_id=category.id, parent_path=path)
                category_data = {
                    'id': category.id,
                    'parent': category.parent_id,
                    'name': category.name,
                    'url': category.url,
                    'path': path,
                    'children': children
                }
                category_tree.append(category_data)
        return category_tree

    categories = Category.objects.all()
    category_tree = build_category_tree(categories)
    
    products = Product.objects.filter(remain__gt=0).order_by('?')[:4]

    return render(
        request,
        'app/catalog.html',
        {
            'title': 'Каталог',
            'year': datetime.now().year,
            'categories': category_tree,
            'products': products,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас',
            'year':datetime.now().year,
        }
    )

def partners(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/partners.html',
        {
            'title':'Партнеры',
            'year':datetime.now().year,
        }
    )


def anketa(request):
    assert isinstance(request, HttpRequest)
    
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {'1': 'Каждый день', '2': 'Несколько раз в день', '3': 'Несколько раз в неделю', '4': 'Несколько раз в месяц'}

    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'city': form.cleaned_data['city'],
                'job': form.cleaned_data['job'],
                'gender': gender.get(form.cleaned_data['gender'], ''),
                'internet': internet.get(form.cleaned_data['internet'], ''),
                'notice': 'Да' if form.cleaned_data['notice'] else 'Нет',
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
        else:
            data = None
    else:
        form = AnketaForm()
        data = None
    
    return render(request, 'app/anketa.html', {'form': form, 'data': data})

def registration(request):
    """Renders the registration page."""
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            regform.last_login = datetime.now()
            
            regform.save()
            
            return redirect("home")
    else:
        regform = UserCreationForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/registration.html",
        {
            'regform': regform,
            'year': datetime.now().year,
            'title':'Регистрация',
        }
    )

def dynamic3(request, item1, item2, item3):
    def find_category_in_tree(category_id, tree):
        for category in tree:
            if category['id'] == category_id:
                return category
            found = find_category_in_tree(category_id, category.get('children', []))
            if found:
                return found
        return None

    def build_category_tree(categories, parent_id=None, parent_path=""):
        category_tree = []
        for category in categories:
            if category.parent_id == parent_id:
                path = f"{parent_path}/{category.url}" if parent_path else category.url
                children = build_category_tree(categories, parent_id=category.id, parent_path=path)
                category_data = {
                    'id': category.id,
                    'parent': category.parent_id,
                    'name': category.name,
                    'url': category.url,
                    'path': path,
                    'children': children
                }
                category_tree.append(category_data)
        return category_tree
    
    def get_category_ids(category_id, tree):
        ids = [category_id]
        for category in tree:
            if category['id'] == category_id:
                for child in category.get('children', []):
                    ids.extend(get_category_ids(child['id'], category.get('children', [])))
        return ids
    
    categories = Category.objects.all()
    category_tree = build_category_tree(categories)
    
    category = Category.objects.filter(url=item1).first()
    
    catalog_history = []
    
    category_data = {
        'id': 0,
        'name': "Страница не найдена",
    }
    
    title = "Ошибка 404"
    
    products = NULL
    paginator = NULL
    # Страница и сортировка
    
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    else:
        try:
            page_number = int(page_number)
            if page_number <= 0:
                page_number = 1
        except ValueError:
            page_number = 1

    sort_param = request.GET.get('sort')
    if not sort_param:
        sort_param = 'price_ASC'
    elif sort_param not in ['price_DESC', 'price_ASC']:
        sort_param = 'price_ASC'

    
    if category:
        catalog_history.append({
            "name": category.name,
            "path": "/catalog/" + category.url + "/"
        })
        category2 = Category.objects.filter(url=item2, parent=category.id).first()
        if (category2):
            catalog_history.append({
                "name": category2.name,
                "path": catalog_history[0]["path"] + category2.url + "/"
            })
            category3 = Category.objects.filter(url=item3, parent=category2.id).first()
            if (category3):
                category_ids = get_category_ids(category3.id, category_tree)
                # Получение продуктов
                items_per_page = 8 

                products = Product.objects.filter(category__in=category_ids)

                if sort_param == 'price_DESC':
                    products = products.order_by('-price')
                else:
                    products = products.order_by('price')

                paginator = Paginator(products, items_per_page)

                try:
                    page = paginator.page(page_number)
                except PageNotAnInteger:
                    page = paginator.page(1)
                except EmptyPage:
                    page = paginator.page(paginator.num_pages)

                page_number = page
                products = page.object_list
                catalog_history.append({
                    "name": category3.name,
                    "path": catalog_history[1]["path"] + category3.url + "/"
                })
                title = category3.name
                category_data = find_category_in_tree(category3.id, category_tree)
    
    context = {
        "title": title,
        "category": category_data,
        "catalog_history": catalog_history,
        "products": products,
        "page": page_number,
        "sort": sort_param,
        "paginator": paginator
    }
    return render(request, 'app/dynamic.html', context)

def dynamic2(request, item1, item2):
    def find_category_in_tree(category_id, tree):
        for category in tree:
            if category['id'] == category_id:
                return category
            found = find_category_in_tree(category_id, category.get('children', []))
            if found:
                return found
        return None

    def build_category_tree(categories, parent_id=None, parent_path=""):
        category_tree = []
        for category in categories:
            if category.parent_id == parent_id:
                path = f"{parent_path}/{category.url}" if parent_path else category.url
                children = build_category_tree(categories, parent_id=category.id, parent_path=path)
                category_data = {
                    'id': category.id,
                    'parent': category.parent_id,
                    'name': category.name,
                    'url': category.url,
                    'path': path,
                    'children': children
                }
                category_tree.append(category_data)
        return category_tree
    
    def get_category_ids(category_id, tree):
        ids = [category_id]
        for categoryParent in tree:
            for category in categoryParent["children"]: 
                if category['id'] == category_id:
                    for child in category.get('children', []):
                        ids.extend(get_category_ids(child['id'], category.get('children', [])))
        return ids

    categories = Category.objects.all()
    category_tree = build_category_tree(categories)
    
    category = Category.objects.filter(url=item1).first()
    
    catalog_history = []

    title = "Ошибка 404"
    
    category_data = {
        'id': 0,
        'name': "Страница не найдена",
    }

    products = NULL
    paginator = NULL
    # Страница и сортировка
    
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    else:
        try:
            page_number = int(page_number)
            if page_number <= 0:
                page_number = 1
        except ValueError:
            page_number = 1

    sort_param = request.GET.get('sort')
    if not sort_param:
        sort_param = 'price_ASC'
    elif sort_param not in ['price_DESC', 'price_ASC']:
        sort_param = 'price_ASC'

    if category:
        catalog_history.append({
            "name": category.name,
            "path": "/catalog/" + category.url + "/"
        })
        category2 = Category.objects.filter(url=item2, parent=category.id).first()
        if (category2):
            category_ids = get_category_ids(category2.id, category_tree)

            # Получение продуктов
            items_per_page = 8 

            products = Product.objects.filter(category__in=category_ids)

            if sort_param == 'price_DESC':
                products = products.order_by('-price')
            else:
                products = products.order_by('price')

            paginator = Paginator(products, items_per_page)

            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)

            page_number = page
            products = page.object_list
            catalog_history.append({
                "name": category2.name,
                "path": catalog_history[0]["path"] + category2.url + "/"
            })
            title = category2.name
            category_data = find_category_in_tree(category2.id, category_tree)
    
    context = {
        "title": title,
        "category": category_data,
        "catalog_history": catalog_history,
        "products": products,
        "page": page_number,
        "sort": sort_param,
        "paginator": paginator
    }
    return render(request, 'app/dynamic.html', context)

def dynamic1(request, item1):
    def find_category_in_tree(category_id, tree):
        for category in tree:
            if category['id'] == category_id:
                return category
            found = find_category_in_tree(category_id, category.get('children', []))
            if found:
                return found
        return None

    def build_category_tree(categories, parent_id=None, parent_path=""):
        category_tree = []
        for category in categories:
            if category.parent_id == parent_id:
                path = f"{parent_path}/{category.url}" if parent_path else category.url
                children = build_category_tree(categories, parent_id=category.id, parent_path=path)
                category_data = {
                    'id': category.id,
                    'parent': category.parent_id,
                    'name': category.name,
                    'url': category.url,
                    'path': path,
                    'children': children
                }
                category_tree.append(category_data)
        return category_tree
    
    def get_category_ids(category_id, tree):
        ids = []
        for category in tree:
            if category['id'] == category_id:
                ids = [category_id]
                for child in category.get('children', []):
                    ids.extend(get_category_ids(child['id'], category.get('children', [])))
        return ids

    categories = Category.objects.all()
    category_tree = build_category_tree(categories)
    
    category = Category.objects.filter(url=item1).first()
    
    catalog_history = []
    
    category_data = {
        'id': 0,
        'name': "Страница не найдена",
    }
    
    title = "Ошибка 404"
    
    products = NULL
    paginator = NULL
    
    # Страница и сортировка
    
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    else:
        try:
            page_number = int(page_number)
            if page_number <= 0:
                page_number = 1
        except ValueError:
            page_number = 1

    sort_param = request.GET.get('sort')
    if not sort_param:
        sort_param = 'price_ASC'
    elif sort_param not in ['price_DESC', 'price_ASC']:
        sort_param = 'price_ASC'

    
    if category:
        category_ids = get_category_ids(category.id, category_tree)
        # Получение продуктов
        items_per_page = 8 

        products = Product.objects.filter(category__in=category_ids)

        if sort_param == 'price_DESC':
            products = products.order_by('-price')
        else:
            products = products.order_by('price')

        paginator = Paginator(products, items_per_page)

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        page_number = page
        products = page.object_list
        catalog_history.append({
            "name": category.name,
            "path": "/catalog/" + category.url + "/"
        })
        title = category.name
        category_data = find_category_in_tree(category.id, category_tree)
   

    context = {
        "title": title,
        "category": category_data,
        "catalog_history": catalog_history,
        "products": products,
        "page": page_number,
        "sort": sort_param,
        "paginator": paginator
    }
    return render(request, 'app/dynamic.html', context)


def products(request, item):
    
    product_data = {
        'id': 0,
        'name': "Страница не найдена",
    }
    
    product = Product.objects.filter(id=item).first()
    products = NULL
    if product: 
        product_data = {
            'id': product.id,
            'name': product.name,
        }

        category = product.category

        category_list = []

        while category:
            category_list.insert(0, {
                "name": category.name,
                "url": category.url
            })
            category = Category.objects.filter(id=category.parent_id).first()

        category_path = "/catalog/"

        catalog_history = []

        print(category_list)

        for cat in category_list:
            category_path += f"{cat['url']}/"
            catalog_history.append({
                "name": cat["name"],
                "path": category_path
            })
            
        products = Product.objects.filter(remain__gt=0).exclude(id=product.id).order_by('?')[:4]   
  
    context = {
        "title": product_data["name"],
        "product_data": product_data,
        "product": product,
        "products": products,
        "catalog_history": catalog_history
    }
    return render(request, 'app/products.html', context)

def cart(request):
    context = {
        "title": "Корзина",
    }
    return render(request, 'app/cart.html', context)

@login_required
def cabinet(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('cabinet')


    else:
        password_form = PasswordChangeForm(request.user)

    active_orders = Order.objects.filter(user=request.user)

    for order in active_orders:
        order.items = OrderProduct.objects.filter(order=order)
        order.total_cost = sum(item.price * item.count for item in order.items)
        
    context = {
        "title": "Кабинет",
        "active_orders": active_orders,
        "form": password_form,
    }
    return render(request, 'app/cabinet.html', context)

def create_order(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cart_items = json.loads(request.body)
            order = Order.objects.create(user=request.user)
            print(cart_items)
            for item in cart_items["cartItems"]:
                product_id = item['id']
                quantity = item['quantity']
                price = item['price']

                price = Decimal(item['price'].replace(',', '.'))

                order_product = OrderProduct.objects.create(order=order, product_id=product_id, count=quantity, price=price)

            request.session['cartItems'] = []

            return JsonResponse({'message': 'Заказ успешно оформлен.'}, status=201)
        else:
            return JsonResponse({'error': 'Пользователь не аутентифицирован.'}, status=401)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST.'}, status=405)
    
@require_POST
def delete_order(request, order_id):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(pk=order_id, user=request.user)
            order.delete()
            return JsonResponse({'message': 'Заказ успешно удален.'}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Указанный заказ не существует или не принадлежит текущему пользователю.'}, status=404)
    else:
        return JsonResponse({'error': 'Пользователь не аутентифицирован.'}, status=401)


def error_404(request, exception):
    return render(request, 'app/404.html', status=404)