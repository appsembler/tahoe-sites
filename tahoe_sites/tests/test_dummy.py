import factory
from django.contrib.auth import get_user_model
from django.test import TestCase
from factory.django import DjangoModelFactory
from organizations.models import Organization

from tahoe_sites.models import TahoeSiteUUID, UserOrganizationMapping


class UserFactory(DjangoModelFactory):
    email = factory.Sequence('robot{}@example.com'.format)
    username = factory.Sequence('robot{}'.format)

    class Meta:
        model = get_user_model()


class TestDummy(TestCase):
    def test_dummy(self):
        self.user = UserFactory.create()
        organization = Organization.objects.create(
            name='test organization',
            description='test organization description',
            active=True
        )
        UserOrganizationMapping.objects.create(
            user=self.user,
            organization=organization,
            is_admin=True,
        )
        TahoeSiteUUID.objects.create(
            organization=organization,
        )
