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
from tahoe_sites.tests.utils import create_organization_mapping
from tahoe_sites.zd_helpers import should_site_use_org_models


class DefaultsForTestsMixin(TestCase):
    """
    Mixin that creates some default objects
    """
    def _create_organization(self, name, short_name, active=True):  # pylint: disable=no-self-use
        return Organization.objects.create(
            name=name,
            description='{name} description'.format(name=name),
            active=active,
            short_name=short_name,
        )

    def setUp(self) -> None:
        """
        Initialization
        """
        self.default_org = self._create_organization(
            name='test organization',
            short_name='TO'
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


class TestTahoeSiteUUID(DefaultsForTestsMixin):
    """
    Tests for TahoeSiteUUID model
    """
    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_create_organization_signal(self):
        """
        Verify that creating an Organization object will signal a creation for TahoeUUISite
        """
        sites_count = TahoeSiteUUID.objects.count()
        organization = self._create_organization(
            name='dummy organization',
            short_name='DO',
        )
        assert TahoeSiteUUID.objects.count() == sites_count + 1
        assert TahoeSiteUUID.objects.get(organization=organization)

    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_save_organization_dose_not_create_site(self):
        """
        Verify that saving an Organization object will not create another TahoeUUISite
        """
        sites_count = TahoeSiteUUID.objects.count()
        organization = self._create_organization(
            name='dummy organization',
            short_name='DO',
        )
        organization.name = 'new name'
        organization.save()
        assert TahoeSiteUUID.objects.count() == sites_count + 1
        assert TahoeSiteUUID.objects.get(organization=organization)
