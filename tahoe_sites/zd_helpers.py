"""
Helpers used for Zero Downtime process. This file should be removed at the end
"""
from django.conf import settings


def should_site_use_org_models():
    return not settings.FEATURES.get('TAHOE_SITES_USE_ORGS_MODELS', True)


def get_meta_managed():
    return not should_site_use_org_models()


def get_db_column(old_column_name):
    return old_column_name if should_site_use_org_models() else None


def get_db_table(old_table_name):
    return old_table_name if should_site_use_org_models() else None
