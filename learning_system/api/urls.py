from django.urls import path
from .views import UserLessonsView, ProductLessonsView, ProductView

urlpatterns = [
    path('lessons/', UserLessonsView.as_view(), name='users_lessons'),
    path('lessons/<int:pk>/', ProductLessonsView.as_view(), name='product_lessons'),
    path('products/', ProductView.as_view(), name='products'),
    
]