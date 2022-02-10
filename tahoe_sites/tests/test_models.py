"""
Tests for models
"""
import pytest
from django.db.utils import IntegrityError
from django.contrib.sites.models import Site
from django.test import TestCase
from organizations.models import Organization

from tahoe_sites.models import TahoeSite, UserOrganizationMapping
from tahoe_sites.tests.fatories import UserFactory
from tahoe_sites.tests.utils import create_organization_mapping
from tahoe_sites.zd_helpers import should_site_use_org_models


class DefaultsForTestsMixin(TestCase):
    """
    Mixin that creates some default objects
    """
    def create_organization(self, name, short_name, active=True):  # pylint: disable=no-self-use
        """
        helper to create an Organization object
        """
        return Organization.objects.create(
            name=name,
            description='{name} description'.format(name=name),
            active=active,
            short_name=short_name,
        )

    def create_django_site(self, domain):  # pylint: disable=no-self-use
        """
        helper to create a Site object
        """
        return Site.objects.create(domain=domain)

    def setUp(self) -> None:
        """
        Initialization
        """
        self.default_org = self.create_organization(
            name='test organization',
            short_name='TO'
        )
        self.default_django_site = self.create_django_site('dummy.com')
        if should_site_use_org_models():
            self.default_tahoe_site = None
            self.default_org.sites.add(self.default_django_site)
        else:
            self.default_tahoe_site = TahoeSite.objects.create(
                organization=self.default_org,
                site=self.default_django_site
            )

        self.default_user = UserFactory.create()


class TestUserOrganizationMapping(DefaultsForTestsMixin):
    """
    Tests for UserOrganizationMapping model
    """
    @pytest.mark.skipif(should_site_use_org_models(), reason='Not implemented in edx-organizations')
    def test_same_user_same_org(self):
        """
        Having the same user for the same organization should not be allowed
        """
        create_organization_mapping(
            user=self.default_user,
            organization=self.default_org,
        )
        assert UserOrganizationMapping.objects.count() == 1

        with self.assertRaisesMessage(
            expected_exception=IntegrityError,
            expected_message='UNIQUE constraint failed: tahoe_sites_userorganizationmapping.user_id,'
        ):
            create_organization_mapping(
                user=self.default_user,
                organization=self.default_org,
            )

    def test_to_string(self):
        """
        Verify format of auto convert to string
        """
        mapping = create_organization_mapping(
            user=self.default_user,
            organization=self.default_org,
        )
        assert str(mapping) == 'UserOrganizationMapping<{email}, {short_name}>'.format(
            email=self.default_user.email,
            short_name=self.default_org.short_name,
        )
