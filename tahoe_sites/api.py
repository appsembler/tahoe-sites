"""
External Python API helpers goes here.

Those APIs should be stable and abstract internal model changes.
Non-stable APIs they should be placed in the `helpers.py` module instead.


### API Contract:

 * The parameters of existing functions should change in a backward compatible way:
   - No parameters should be removed from the function
   - New parameters should have safe defaults
 * For breaking changes, new functions should be created
"""
import organizations.api
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
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


def create_tahoe_site(domain, short_name, site_uuid=None):
    """
    Centralized method to create the site objects in both `tahoe-sites` and `edx-organizations`.

    Other pieces like SiteConfigurations are out of the scope of this helper.

    :param domain: Site domain.
    :param short_name: Organization short name, course key component and site name.
    :param site_uuid: UUID string or object. Used to identify organizations and sites across Tahoe services.
    :return: dict with `site` `organization` and `site_uuid` fields.
    """
    site = Site.objects.create(domain=domain, name=short_name)

    organization_data = {
        'name': short_name,
        'short_name': short_name,
        'description': 'Organization of {domain} (automatic)'.format(domain=site.domain),
    }

    if site_uuid and zd_helpers.should_site_use_org_models():
        organization_data['edx_uuid'] = site_uuid

    organization_serialized = organizations.api.add_organization(organization_data)
    organization = Organization.objects.get(pk=organization_serialized['id'])

    if zd_helpers.should_site_use_org_models():
        returned_uuid = organization.edx_uuid
    else:
        link = TahoeSiteUUID.objects.create(
            organization=organization,
            site_uuid=site_uuid,
        )
        returned_uuid = link.site_uuid

    return {
        'site_uuid': returned_uuid,
        'site': site,
        'organization': organization,
    }


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


def is_active_admin_on_any_organization(user, org_ids):
    """
    Check if the given user is an admin on any of the given organizations

    :param user: user to filter on
    :param org_ids: QuerySet of organization ids to filter on
    :return: <True> if user is an admin on any organization, <False> otherwise
    """
    return UserOrganizationMapping.objects.filter(
        user=user,
        organization_id__in=org_ids,
        is_active=True,
        is_admin=True,
    ).exists()


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
