from factory.django import DjangoModelFactory
from users.models import Profile
import factory
from .user_factory import UserFactory


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    occupation = "Lawyer"
