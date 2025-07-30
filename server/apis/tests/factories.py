import factory
from faker import Factory as FakerFactory

from apis.models import User

faker = FakerFactory.create()

class UserFactory(factory.django.DjangoModelFactory):
    email = factory.LazyAttribute(lambda x: faker.email())
    
    class Meta:
        model = User
    