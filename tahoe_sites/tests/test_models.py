"""
Tests for models
"""
import pytest
from django.conf import settings
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
    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_get_organization_by_uuid_without_org(self):
        """
        Test get_organization_by_uuid helper when edx-organizations customization is off
        """
        default_site = TahoeSiteUUID.objects.get(organization=self.default_org)
        assert TahoeSiteUUID.get_organization_by_uuid(default_site.site_uuid) == self.default_org

    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_get_uuid_by_organization_without_org(self):
        """
        Test get_uuid_by_organization helper when edx-organizations customization is off
        """
        default_site = TahoeSiteUUID.objects.get(organization=self.default_org)
        assert TahoeSiteUUID.get_uuid_by_organization(self.default_org) == default_site.site_uuid

    @pytest.mark.skipif(not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is on')
    def test_get_organization_by_uuid_with_org(self):
        """
        Test get_organization_by_uuid helper when edx-organizations customization is on
        """
        assert TahoeSiteUUID.get_organization_by_uuid(self.default_org.edx_uuid) == self.default_org

    @pytest.mark.skipif(not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is on')
    def test_get_uuid_by_organization_with_org(self):
        """
        Test get_uuid_by_organization helper when edx-organizations customization is on
        """
        assert TahoeSiteUUID.get_uuid_by_organization(self.default_org) == self.default_org.edx_uuid

    @staticmethod
    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_create_organization_signal():
        """
        Verify that creating an Organization object will signal a creation for TahoeUUISite
        """
        sites_count = TahoeSiteUUID.objects.count()
        organization = Organization.objects.create(
            name='dummy organization',
            description='dummy organization description',
            active=True,
            short_name='DO',
        )
        assert TahoeSiteUUID.objects.count() == sites_count + 1
        assert TahoeSiteUUID.objects.get(organization=organization)

    @staticmethod
    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_save_organization_dose_not_create_site():
        """
        Verify that saving an Organization object will not create another TahoeUUISite
        """
        sites_count = TahoeSiteUUID.objects.count()
        organization = Organization.objects.create(
            name='dummy organization',
            description='dummy organization description',
            active=True,
            short_name='DO',
        )
        organization.name = 'new name'
        organization.save()
        assert TahoeSiteUUID.objects.count() == sites_count + 1
        assert TahoeSiteUUID.objects.get(organization=organization)
