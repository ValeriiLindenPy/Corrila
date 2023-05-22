from django.contrib import admin

from .models import *

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}

admin.site.register(Report)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Feedback)

