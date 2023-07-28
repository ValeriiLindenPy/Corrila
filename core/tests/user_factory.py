from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
import factory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = "Jonny"
    email = "tset@gmail.com"
    password = factory.django.Password("Xyz12234")
