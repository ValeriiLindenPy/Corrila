# Generated by Django 4.0.5 on 2023-05-19 10:44

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_firs_tname_feedback_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=ckeditor.fields.RichTextField(default='Write somthing about statisics or correlation', null=True),
        ),
    ]
