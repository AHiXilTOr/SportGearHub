from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

#Страница "Помощь"
def help(request):
    context = {'title': 'Помощь'}
    return render(request, 'help.html', context)

#Страница "Главная"
def index(request):
    context = {'title': 'Главная'}
    return render(request, 'index.html', context)

#Страница "Каталог"
def catalog(request):
    context = {'title': 'Каталог'}
    return render(request, 'catalog.html', context)

#Страница "Политика Конфиденциальности"
def privacy(request):
    context = {'title': 'Политика конфиденциальности'}
    return render(request, 'privacy.html', context)

#Страница "О нас"
def aboutus(request):
    context = {'title': 'О нас'}
    return render(request, 'aboutus.html', context)

#Страница "Контакты"
def contacts(request):
    context = {'title': 'Контакты'}
    return render(request, 'contacts.html', context)

#Страница "Товары"
def products(request):
    products = Product.objects.all()
    producer_tb = Brand.objects.only('name')
    category_tb = Category.objects.only('name')
    material_tb = Material.objects.only('name')
    color_tb = Color.objects.only('name')

    #Объявление переменных
    bonus = range(4)
    material_selected = 0
    category_selected = 0
    brand_selected = 0
    color_selected = 0

    #Получение списка категорий
    material = request.GET.get('material', None)
    category = request.GET.get('category', None)
    producer = request.GET.get('producer', None)
    color = request.GET.get('color', None)

    #Фильтрация по категории
    if material and material != '0':
        products = products.filter(material=material)
        material_selected = material
    if category and category != '0':
        products = products.filter(category=category)
        category_selected = category
    if producer and producer != '0':
        products = products.filter(brand=producer)
        brand_selected = producer
    if color and color != '0':
        products = products.filter(productcolor__color=color)
        color_selected = color

    #Получение состояния сортировки
    sort_state_a = request.GET.get('sort_state_a', 'asc')
    sort_state_b = request.GET.get('sort_state_b', 'asc')
    sort_a = request.GET.get('sort-a', None)
    sort_b = request.GET.get('sort-b', None)

    #Проверка состояния сортировки
    if sort_a:
        if sort_state_a == 'asc':
            products = products.order_by('-name')
            sort_state_a = 'desc'
        else:
            products = products.order_by('name')
            sort_state_a = 'asc'
    if sort_b:
        if sort_state_b == 'asc':
            products = products.order_by('-price')
            sort_state_b = 'desc'
        else:
            products = products.order_by('price')
            sort_state_b = 'asc'

    context = {'title': 'Товары',
               'producer': producer_tb,
               'category': category_tb,
               'material': material_tb,
               'color': color_tb,
               'material_selected': int(material_selected),
               'category_selected': int(category_selected),
               'brand_selected': int(brand_selected),
               'color_selected': int(color_selected),
               'products': products,
               'bonus': bonus,
               'sort_state_a': sort_state_a,
               'sort_state_b': sort_state_b}
    return render(request, 'inheritance/products.html', context)

#Страница "Товара"
def product(request, id):
    context = {'title': 'Товар'}
    product = Product.objects.filter(product_id=id)
    product_attributes = ProductAttribute.objects.filter(product_id=id).values('attribute__name__name', 'value', 'attribute__unit__unit')
    print(product_attributes.query)
    context = {
        'title': 'Товар',
        'product': product,
        'product_attributes': product_attributes}
    return render(request, 'inheritance/product.html', context)

#Проверка с помощью декоратора метода POST
@require_http_methods(['POST'])
def create_object_view(request):
    try:
        feed = request.POST.get('feed')
        feed = RequestType.objects.get(request_type_id=int(feed))
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(type_of_request=feed, first_name=firstName,
                          last_name=lastName or None, email=email, phone=phone or None, message=message)
        contact.save()
        data = {'success': True}
    except Exception as e:
        data = {'error': str(e)}
    return JsonResponse(data)

#Страница "Поиск"
def search(request):
    producer_tb = Brand.objects.only('name')
    category_tb = Category.objects.only('name')
    material_tb = Material.objects.only('name')
    color_tb = Color.objects.only('name')

    #Объясвление переменных
    bonus = range(4)
    material_selected = 0
    category_selected = 0
    brand_selected = 0
    color_selected = 0
    sort_state_a = 'asc'
    sort_state_b = 'asc'

    #Получение строки поиска
    query = request.GET.get('query', None)
    results = []

    #Проверка строки поиска на совпадение в БД
    if query:
        search_terms = query.split()
        for term in search_terms:
            products = Product.objects.filter(
                Q(name__icontains=term) |
                Q(description__icontains=term) |
                Q(price__icontains=term) |
                Q(warranty_months__icontains=term))
            results.extend(products)

    count = len(results) if results else 0
    context = {
        'title_search': f'По запросу «{query}» было найдено {count} товар ',
        'title': 'Поиск',
        'products': results,
        'bonus': bonus,
        'producer': producer_tb,
        'category': category_tb,
        'material': material_tb,
        'color': color_tb,
        'material_selected': int(material_selected),
        'category_selected': int(category_selected),
        'brand_selected': int(brand_selected),
        'color_selected': int(color_selected),
        'sort_state_a': sort_state_a,
        'sort_state_b': sort_state_b}
    return render(request, 'inheritance/products.html', context)
