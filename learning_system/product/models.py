from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'
    
class Access(models.Model):
    class Status(models.TextChoices):
        ADMIN ='AD', 'Admin'
        USER = 'US', 'User'

    product = models.ForeignKey(Product, related_name='access', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='access', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices)

    class Meta:
        unique_together = ['product', 'user']

    def __str__(self):
        return f'{self.product.title} {self.user.username}'

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    duration = models.IntegerField() 
    products = models.ManyToManyField(Product, related_name='lessons')
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

class LessonWatchTime(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='lwt', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_spent = models.IntegerField(default=0)
    watched = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} {self.lesson}'