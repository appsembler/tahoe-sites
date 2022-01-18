"""
Helpers used for Zero Downtime process. This file should be removed at the end
"""
from django.conf import settings


def should_site_use_org_models():
    """
    Returns the value of TAHOE_SITES_USE_ORGS_MODELS feature flag
    """
    return settings.FEATURES.get('TAHOE_SITES_USE_ORGS_MODELS', True)


def get_meta_managed():
    """
    According to the value of TAHOE_SITES_USE_ORGS_MODELS feature flag
    Return True is the flag is set, otherwise return False
    """
    return not should_site_use_org_models()


def get_replacement_name(old_name):
    """
    According to the value of TAHOE_SITES_USE_ORGS_MODELS feature flag
    Used for database migration and declaration. Returns the given string only if the flag is set
    """
    return old_name if should_site_use_org_models() else None


def get_unique_together(unique_together):
    """
    According to the value of TAHOE_SITES_USE_ORGS_MODELS feature flag
    Used for database migration and declaration. Returns the given field names only if the flag is NOT set
    """
    return unique_together if not should_site_use_org_models() else None
