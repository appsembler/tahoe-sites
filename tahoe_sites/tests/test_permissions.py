from django.contrib.sites.models import Site
from django.test import TestCase
from organizations.tests.factories import UserFactory, OrganizationFactory
from rest_framework.test import APIRequestFactory

from tahoe_sites.models import UserOrganizationMapping

from tahoe_sites.permissions import IsSiteAdminPermission


class SiteAdminPermissionsTestCase(TestCase):
    """
    Verify permissions for AMC users.

    # TODO: Move me into Tahoe-sites.

    If the user is an admin user of an organization, they should be able to have access.
    """

    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()
        self.site = Site.object.create(domain='foo.dev', name='foo.dev')
        factory = APIRequestFactory()
        self.request = factory.get('/test/')
        self.request.user = self.user
        self.organization = OrganizationFactory()

    def test_random_user(self):
        assert not IsSiteAdminPermission().has_permission(self.request, view=None)

    def test_organization_nonadmin_user(self):
        UserOrganizationMapping.objects.create(user=self.user, organization=self.organization, is_admin=False)
        assert not IsSiteAdminPermission().has_permission(self.request, view=None)

    def test_organization_admin_user(self):
        UserOrganizationMapping.objects.create(user=self.user, organization=self.organization, is_admin=True)
        assert IsSiteAdminPermission().has_permission(self.request, view=None)
