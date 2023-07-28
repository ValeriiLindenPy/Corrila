from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
import factory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.sequence(lambda n: f"test{n}@example.com")
    password = factory.django.Password("my_password")
