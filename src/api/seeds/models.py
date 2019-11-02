import factory
from django.contrib.auth.models import User
from faker import Factory

from api.constants import INSERTED
from api.models import *

faker = Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.LazyAttribute(
        lambda _: faker.first_name())
    last_name = factory.LazyAttribute(
        lambda _: faker.last_name())
    email = username = factory.LazyAttribute(
        lambda _: faker.email())
    password = factory.PostGenerationMethodCall(
        'set_password',
        faker.password(
            length=10,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )
    )

    @classmethod
    def generate_JSON(cls):
        email = username = faker.email()
        return {
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'email': email,
            'username': username,
            'password': faker.password(
                length=10,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            )
        }


class WorkflowFactory(factory.DjangoModelFactory):
    class Meta:
        model = Workflow

    status = INSERTED
    data = factory.LazyAttribute(lambda _: faker.pylist(
        10, False, 'str'))
    steps = factory.LazyAttribute(
        lambda _: faker.pylist(10, False, 'str'))
    created_by = factory.SubFactory(UserFactory)
    produced_by = factory.SubFactory(UserFactory)

    @classmethod
    def generate_JSON(cls):
        return {
            'data': faker.pydict(10, False, 'str'),
            'steps': faker.pylist(10, False, 'str')
        }
