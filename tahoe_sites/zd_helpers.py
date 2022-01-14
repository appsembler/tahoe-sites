"""
Helpers used for Zero Downtime process. This file should be removed at the end
"""
from django.conf import settings


def get_meta_managed():
    return not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS']


def get_db_column(old_column_name):
    return old_column_name if settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'] else None


def get_db_table(old_table_name):
    return old_table_name if settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'] else None
