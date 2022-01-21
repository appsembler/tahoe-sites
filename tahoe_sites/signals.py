"""
Signals used to sync with Organization model
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from organizations.models import Organization

from tahoe_sites import zd_helpers
from tahoe_sites.models import TahoeSiteUUID


@receiver(post_save, sender=Organization)
def auto_create_tahoe_site_uuid(instance, created, **kwargs):
    """
    Create TahoeSiteUUID for every new Organization
    """
    if created and not zd_helpers.should_site_use_org_models():
        TahoeSiteUUID.objects.get_or_create(
            organization=instance,
        )
