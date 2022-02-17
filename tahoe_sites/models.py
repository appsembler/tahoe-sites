"""
Package models goes here
"""
import uuid

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.utils import IntegrityError
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

    def __str__(self):
        """
        Converts the object into a string

        :return: string representation of the object
        """
        return 'UserOrganizationMapping<{email}, {organization}>'.format(
            email=self.user.email,  # pylint: disable=no-member
            organization=self.organization.short_name,
        )

    @classmethod
    def is_user_already_mapped(cls, user):
        """
        Check if the user already mapped to an organization or not (regardless of active/admin statuses)

        :param user: User to check
        :return: <True> if the user already mapped to an organization, <False> otherwise
        """
        return cls.objects.filter(user=user).count() > 0

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override save to control user uniqueness rule

        :param force_insert: inherited
        :param force_update: inherited
        :param using: inherited
        :param update_fields: inherited
        :return: inherited
        """
        if not self.pk and self.is_user_already_mapped(user=self.user):
            raise IntegrityError('Cannot add user to organization. User already added to an organization!')

        super().save(force_insert, force_update, using, update_fields)


class TahoeSite(models.Model):
    """
    Handle Site UUID
    """
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
    )
    site_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = 'tahoe_sites'
