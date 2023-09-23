from rest_framework import serializers
from product.models import LessonWatchTime, Lesson, Product

class LessonsWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonWatchTime
        fields = '__all__'

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'duration',)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'