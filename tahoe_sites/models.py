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
        db_column=zd_helpers.get_db_column('is_amc_admin'),
    )

    class Meta:
        app_label = 'tahoe_sites'
        managed = zd_helpers.get_meta_managed()
        db_table = zd_helpers.get_db_table('organizations_userorganizationmapping')

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
