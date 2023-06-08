from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=250, blank=False)
    preview_text = models.TextField(
        blank=False, default='Somthing intresting inside the article. Just read it!')
    text = RichTextField(blank=False, null=True,
                         default='Write somthing about statisics or correlation')
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    pubplication_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    moderated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})


class Report(models.Model):
    title = models.CharField(max_length=250, blank=True)
    low_correlaton_result = models.TextField()
    high_correlaton_result = models.TextField()
    correlatons_range = models.CharField(max_length=250, blank=True)
    correlaton_type = models.CharField(max_length=250)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    pubplication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report of user {self.author} named "{self.title}" - {self.pubplication_date}'

    def get_absolute_url(self):
        return reverse('report', kwargs={'report_id': self.pk})


class Feedback(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    message = models.TextField(max_length=1000)
    sending_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.email} - {self.sending_date}'
    
    
class TemporaryFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
