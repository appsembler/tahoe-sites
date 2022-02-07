"""
Tests for models
"""
import pytest
from django.conf import settings
from organizations.models import Organization

from tahoe_sites import api
from tahoe_sites.models import TahoeSiteUUID
from tahoe_sites.tests.fatories import UserFactory
from tahoe_sites.tests.test_models import DefaultsForTestsMixin
from tahoe_sites.tests.utils import create_organization_mapping


class TestAPIHelpers(DefaultsForTestsMixin):
    """
    Tests for API helpers
    """
    def setUp(self):
        super().setUp()
        self.org1 = None
        self.org2 = None
        self.mapping = None
        self.user2 = None

    def _prepare_mapping_data(self):
        """
        mapping:
            default_org --> default_user
            Org1        --> default_user  -----> self.mapping points here
            Org1        --> user2
            Org2        --> user2
            Org3        --> None
        """
        self.org1 = self._create_organization(name='Org1', short_name='O1')
        create_organization_mapping(user=self.default_user, organization=self.default_org)
        self.mapping = create_organization_mapping(user=self.default_user, organization=self.org1)

        self.org2 = self._create_organization(name='Org2', short_name='O2')
        self.user2 = UserFactory.create()
        create_organization_mapping(user=self.user2, organization=self.org1)
        create_organization_mapping(user=self.user2, organization=self.org2)

        self._create_organization(name='Org3', short_name='O3')

        # We have four organizations
        assert Organization.objects.count() == 4

    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_get_organization_by_uuid_without_org(self):
        """
        Test get_organization_by_uuid helper when edx-organizations customization is off
        """
        default_site = TahoeSiteUUID.objects.get(organization=self.default_org)
        assert api.get_organization_by_uuid(default_site.site_uuid) == self.default_org

    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_get_uuid_by_organization_without_org(self):
        """
        Test get_uuid_by_organization helper when edx-organizations customization is off
        """
        default_site = TahoeSiteUUID.objects.get(organization=self.default_org)
        assert api.get_uuid_by_organization(self.default_org) == default_site.site_uuid

    @pytest.mark.skipif(not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is on')
    def test_get_organization_by_uuid_with_org(self):
        """
        Test get_organization_by_uuid helper when edx-organizations customization is on
        """
        assert api.get_organization_by_uuid(self.default_org.edx_uuid) == self.default_org

    @pytest.mark.skipif(not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is on')
    def test_get_uuid_by_organization_with_org(self):
        """
        Test get_uuid_by_organization helper when edx-organizations customization is on
        """
        assert api.get_uuid_by_organization(self.default_org) == self.default_org.edx_uuid

    def test_get_organizations_for_user_default(self):
        """
        Verify that get_active_organizations_for_user helper returns only related to active user
        """
        self._prepare_mapping_data()

        # default_user is mapped to 2 of them
        assert list(api.get_organizations_for_user(self.default_user)) == [self.default_org, self.org1]

        # user2 is mapped to two of them, one shared with default_user
        assert list(api.get_organizations_for_user(self.user2)) == [self.org1, self.org2]

        # records with inactive user will not be returned
        self.mapping.is_active = False
        self.mapping.save()
        assert list(api.get_organizations_for_user(self.default_user)) == [self.default_org]

    def test_get_organizations_for_user_with_inactive_users(self):
        """
        Verify that get_active_organizations_for_user helper can return all organization related to a user
        including organizations having that user deactivated
        """
        self._prepare_mapping_data()

        self.mapping.is_active = False
        self.mapping.save()
        assert list(api.get_organizations_for_user(self.default_user, with_inactive_users=True)) == [
            self.default_org,
            self.org1
        ]

    def test_get_organizations_for_user_without_admins(self):
        """
        Verify that get_active_organizations_for_user helper can return all organization related to a user
        excluding organizations having that user as an admin
        """
        self._prepare_mapping_data()

        self.mapping.is_admin = True
        self.mapping.save()
        assert list(api.get_organizations_for_user(self.default_user, without_admins=True)) == [self.default_org]

    def test_get_users_of_organization(self):
        """
        Verify that get_users_of_organization returns all active users related to an organization
        """
        self._prepare_mapping_data()

        # default_org is mapped to default_user
        assert list(api.get_users_of_organization(self.default_org)) == [self.default_user]

        # Org1 is mapped to two users
        assert list(api.get_users_of_organization(self.org1)) == [self.default_user, self.user2]

        # inactive users will not be returned
        self.mapping.is_active = False
        self.mapping.save()
        assert list(api.get_users_of_organization(self.org1)) == [self.user2]

    def test_get_users_of_organization_with_inactive_users(self):
        """
        Verify that get_users_of_organization helper can return all user related to an organization
        including deactivated users
        """
        self._prepare_mapping_data()

        self.mapping.is_active = False
        self.mapping.save()
        assert list(api.get_users_of_organization(self.org1, with_inactive_users=True)) == [
            self.default_user,
            self.user2
        ]

    def test_get_users_of_organization_without_admins(self):
        """
        Verify that get_users_of_organization helper can return all user related to an organization
        excluding admin users
        """
        self._prepare_mapping_data()

        self.mapping.is_admin = True
        self.mapping.save()
        assert list(api.get_users_of_organization(self.org1, without_admins=True)) == [self.user2]

    def test_is_active_admin_on_organization(self):
        """
        Verify that is_active_admin_on_organization helper returns True if the given user
        is an admin on the given organization
        """
        self._prepare_mapping_data()

        assert not api.is_active_admin_on_organization(user=self.default_user, organization=self.org1)

        self.mapping.is_admin = True
        self.mapping.save()
        assert api.is_active_admin_on_organization(user=self.default_user, organization=self.org1)
