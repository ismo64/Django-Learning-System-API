from django.shortcuts import render
import json
# Create your views here.
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import RegisterUserForm
from django.contrib.auth import login, authenticate, logout

from django.views.decorators.csrf import csrf_exempt

from .models import Product, Lesson, LessonWatchTime, Access

# Create your views here.

def index(request):
    products = Product.objects.all()
    paginator = Paginator(products, 3)
    page = paginator.page(request.GET.get('page', 1))
    return render(request, 'product/home.html', {'products': page})

def add_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'product/register.html', {'form': form})

def add_access(request, pk):
    access = Access.objects.create(product=Product.objects.get(id=pk), user=request.user, status='US')
    return redirect('show_lessons', pk)

def show_lessons(request, pk):
    product = Product.objects.get(id=pk)
    if request.user.is_authenticated:
        has_access = product.access.filter(user=request.user)
    else:
        return redirect('login')
    print(has_access)
    lessons = Lesson.objects.filter(products__id=pk)
    return render(request, 'product/show_lessons.html', {'lessons': lessons, 
                                                         'pk': pk, 'has_access': has_access})


@csrf_exempt
def lesson_detail(request, pk, lesson_id):
    product = Product.objects.get(id=pk)
    has_access = product.access.filter(user=request.user)
    if not has_access:
        return redirect('show_lessons', pk)
    lesson = Lesson.objects.get(id=lesson_id)
    url = lesson.video_url.split('=')[-1]
    try:
        lwt = LessonWatchTime.objects.get(lesson=lesson_id, user=request.user)
        print(lwt.time_spent)
    except:
        lwt = LessonWatchTime(lesson=lesson, user=request.user)
        lwt.save()

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        time_spent = data['time_spent']
        lwt.time_spent = lwt.time_spent + int(time_spent)
        if (lwt.time_spent / lesson.duration) >= 0.8:
            lwt.watched = True
        lwt.save()

    return render(request, 'product/lesson_detail.html', 
                  {'lesson': lesson, 'product_id': pk, 'url': url, 'lwt': lwt})


def user_products(request, pk):
    products = Product.objects.filter(author__id=pk)
    return render(request, 'product/user_products.html', {'products': products})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'product/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')
