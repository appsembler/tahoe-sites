""" Django admin pages for organization models """
from django.contrib import admin

from tahoe_sites.models import UserOrganizationMapping


@admin.register(UserOrganizationMapping)
class UserOrganizationMappingAdmin(admin.ModelAdmin):
    """
    Many to many admin for Organization/User membership.
    """
    list_display = [
        'email',
        'username',
        'organization_name',
        'is_active',
        'is_admin',
    ]

    search_fields = [
        'user__email',
        'user__username',
        'organization__name',
        'organization__short_name',
    ]

    list_filter = [
        'is_active',
        'is_admin',
    ]

    def email(self, mapping):
        """Display user email."""
        return mapping.user.email

    def username(self, mapping):
        """Display username."""
        return mapping.user.username

    def organization_name(self, mapping):
        """Display organization name."""
        return mapping.organization.short_name
