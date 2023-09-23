from django.contrib import admin
from .models import Product, Access, Lesson, LessonWatchTime

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class LessonAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Lesson
        fields = '__all__'

        
admin.site.register(Product)

admin.site.register(Access)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)
    form = LessonAdminForm

admin.site.register(LessonWatchTime)