"""
Package helper methods goes here
"""
from django.contrib.auth import get_user_model
from organizations.models import Organization

from tahoe_sites import zd_helpers
from tahoe_sites.models import TahoeSiteUUID, UserOrganizationMapping


def get_organization_by_uuid(organization_uuid):
    """
    Get an organization object from it's uuid

    :param organization_uuid: uuid to filter on
    :return: organization of the given uuid
    """
    if zd_helpers.should_site_use_org_models():
        return Organization.objects.get(edx_uuid=organization_uuid)
    return TahoeSiteUUID.objects.get(site_uuid=organization_uuid).organization


def get_uuid_by_organization(organization):
    """
    Get the uuid when from it's related organization

    :param organization: organization to filter on
    :return: uuid of the given organization
    """
    if zd_helpers.should_site_use_org_models():
        return organization.edx_uuid
    return TahoeSiteUUID.objects.get(organization=organization).site_uuid


def get_organizations_for_user(user, with_inactive_users=False, without_admins=False):
    """
    Return organizations related to the given user. By default, the list will ignore
    organizations where the user is inactive

    :param user: user to filter on
    :param with_inactive_users: include organizations where the user is inactive (default = False)
    :param without_admins: exclude organizations where the user is set as admin (default = False)
    :return: Organization objects related to the given user
    """
    if with_inactive_users:
        extra_params = {}
    else:
        extra_params = {'is_active': True}
    if without_admins:
        extra_params['is_admin'] = False

    return Organization.objects.filter(
        pk__in=UserOrganizationMapping.objects.filter(user=user, **extra_params).values('organization_id')
    )


def get_users_of_organization(organization, with_inactive_users=False, without_admins=False):
    """
    Return users related to the given organization. By default, all active users will be
    returned including admin users

    :param organization: organization to filter on
    :param with_inactive_users: include inactive users in the result (default = False)
    :param without_admins: exclude admin users from the result (default = False)
    :return: User objects related to the given organization
    """
    if with_inactive_users:
        extra_params = {}
    else:
        extra_params = {'is_active': True}
    if without_admins:
        extra_params['is_admin'] = False
    return get_user_model().objects.filter(
        pk__in=UserOrganizationMapping.objects.filter(organization=organization, **extra_params).values('user_id')
    )


def is_active_admin_on_organization(user, organization):
    """
    Check if the given user is an admin on the given organizations
    :param user: user to filter on
    :param organization:  organization to filter on
    :return: <True> if user is an admin on the organization, <False> otherwise
    """
    return UserOrganizationMapping.objects.filter(
        user=user,
        organization=organization,
        is_active=True,
        is_admin=True,
    ).exists()
