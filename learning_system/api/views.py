from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product,LessonWatchTime, Access, User
from .serializers import LessonsWatchSerializer, LessonsSerializer, ProductSerializer

# Create your views here.


class UserLessonsView(APIView):
    def get(self, request):
        lessons = LessonWatchTime.objects.filter(user=request.user)
        data = LessonsWatchSerializer(lessons, many=True).data
        for lesson, d in zip(lessons, data):
            d['products'] = [product.title for product in lesson.lesson.products.all()]
        return Response({'lessons': data})

class ProductLessonsView(APIView):
    def get(self, request, pk):
        lessons = Product.objects.get(pk=pk).lessons.all()
        data = LessonsSerializer(lessons, many=True).data
        for lesson, d in zip(lessons, data):
            try:
                lwt = LessonWatchTime.objects.get(lesson=lesson, user=request.user)
            except:
                lwt = LessonWatchTime.objects.create(lesson=lesson, user=request.user)
            d['watched'] = lwt.watched
            d['time_spent'] = lwt.time_spent
            d['last_watched'] = lwt.last_watched

        return Response({'lessons': data})

class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        for product, d in zip(products, data):
            lessons = product.lessons.all()
            watched_lessons_num = 0
            total_watch_time = 0
            for lesson in lessons:
                watched_lessons_num += lesson.lwt.filter(watched=True).count()
                total_watch_time += sum(i['time_spent'] for i in lesson.lwt.all().values('time_spent')) 
            d['watched_lessons_num'] = watched_lessons_num
            d['total_watch_time'] = total_watch_time
            d['total_students'] = Access.objects.filter(product=product).count()
            d['buy_statistics'] = str(round(d['total_students'] / User.objects.all().count(), 2) * 100) + '%'
        return Response({'products': data})
