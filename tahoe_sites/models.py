"""
Package models goes here
"""
import uuid

from django.conf import settings
from django.db import models
from organizations.models import Organization

from tahoe_sites import zd_helpers


class UserOrganizationMapping(models.Model):
    """
    User membership in an organization.

    Tahoe's fundamental multi-site relationship.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='+')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(
        default=False,
        # TODO: Remove once we migrate off edx-organizations tables
        db_column=zd_helpers.get_replacement_name('is_amc_admin'),
    )

    class Meta:
        app_label = 'tahoe_sites'
        managed = zd_helpers.get_meta_managed()
        db_table = zd_helpers.get_replacement_name('organizations_userorganizationmapping')
        unique_together = zd_helpers.get_unique_together(('user', 'organization'))

    def __str__(self):
        return 'UserOrganizationMapping<{email}, {organization}>'.format(
            email=self.user.email,  # pylint: disable=no-member
            organization=self.organization.short_name,
        )


class TahoeSiteUUID(models.Model):
    """
    Handle Site UUID
    """
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
    )
    site_uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        app_label = 'tahoe_sites'

    @classmethod
    def get_organization_by_uuid(cls, organization_uuid):
        """
        Get an organization object from it's uuid
        """
        if zd_helpers.should_site_use_org_models():
            return Organization.objects.get(edx_uuid=organization_uuid)
        return cls.objects.get(site_uuid=organization_uuid).organization

    @classmethod
    def get_uuid_by_organization(cls, organization):
        """
        Get the uuid when from it's related organization
        """
        if zd_helpers.should_site_use_org_models():
            return organization.edx_uuid
        return cls.objects.get(organization=organization).site_uuid
