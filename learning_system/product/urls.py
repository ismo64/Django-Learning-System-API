from django.urls import path
from product import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('register/', views.add_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('products/<int:pk>/', views.user_products, name='user_products'),
    path('lessons/<int:pk>/', views.show_lessons, name='show_lessons'),
    path('lessons/<int:pk>/<int:lesson_id>', views.lesson_detail, name='lesson_detail'),
    path('add_access/<int:pk>', views.add_access, name='access'),
]