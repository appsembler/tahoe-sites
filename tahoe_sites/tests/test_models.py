"""
Tests for models
"""
import pytest
from django.db.utils import IntegrityError
from django.test import TestCase
from organizations.models import Organization

from tahoe_sites.models import TahoeSiteUUID, UserOrganizationMapping
from tahoe_sites.tests.fatories import UserFactory
from tahoe_sites.zd_helpers import should_site_use_org_models


class DefaultsForTestsMixin(TestCase):
    """
    Mixin that creates some default objects
    """
    def setUp(self) -> None:
        """
        Initialization
        """
        self.default_org = Organization.objects.create(
            name='test organization',
            description='test organization description',
            active=True,
            short_name='TO',
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
        UserOrganizationMapping.objects.create(
            user=self.default_user,
            organization=self.default_org,
            is_admin=True,
        )
        assert UserOrganizationMapping.objects.count() == 1

        with self.assertRaisesMessage(
            expected_exception=IntegrityError,
            expected_message='UNIQUE constraint failed: tahoe_sites_userorganizationmapping.user_id,'
        ):
            UserOrganizationMapping.objects.create(
                user=self.default_user,
                organization=self.default_org,
                is_admin=True,
            )

    def test_to_string(self):
        """
        Verify format of auto convert to string
        """
        mapping = UserOrganizationMapping.objects.create(
            user=self.default_user,
            organization=self.default_org,
            is_admin=True,
        )
        assert str(mapping) == 'UserOrganizationMapping<{email}, {short_name}>'.format(
            email=self.default_user.email,
            short_name=self.default_org.short_name,
        )


class TestTahoeSiteUUID(DefaultsForTestsMixin):
    """
    Tests for TahoeSiteUUID model
    """
    def setUp(self) -> None:
        """
        Initialization
        """
        super().setUp()
        self.default_site = TahoeSiteUUID.objects.create(
            organization=self.default_org,
        )

    def test_get_organization_by_uuid(self):
        """
        Test get_organization_by_uuid helper
        """
        assert self.default_site.get_organization_by_uuid(self.default_site.site_uuid) == self.default_org

    def test_get_uuid_by_organization(self):
        """
        Test get_uuid_by_organization helper
        """
        assert self.default_site.get_uuid_by_organization(self.default_site.organization) == self.default_site.site_uuid
