"""
Tests for helper methods
"""
import pytest
from django.conf import settings
from django.test import SimpleTestCase

from tahoe_sites import zd_helpers
from tahoe_sites.helpers import get_organization_by_uuid
from tahoe_sites.models import TahoeSiteUUID
from tahoe_sites.tests.test_models import DefaultsForTestsMixin


class TestHelpers(DefaultsForTestsMixin):
    def test_get_organization_by_uuid(self):
        """
        Test get_organization_by_uuid helper
        """
        site = TahoeSiteUUID.objects.create(
            organization=self.default_org,
        )
        assert get_organization_by_uuid(site.site_uuid) == self.default_org


@pytest.mark.skipif(not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                    reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is on')
class TestZDHelpersWithOrgs(SimpleTestCase):
    """
    Test ZDHelpers when TAHOE_SITES_USE_ORGS_MODELS flag is On
    """
    def test_should_site_use_org_models(self):
        """
        Test should_site_use_org_models
        """
        assert zd_helpers.should_site_use_org_models()

    def test_get_meta_managed(self):
        """
        Test get_meta_managed
        """
        assert not zd_helpers.get_meta_managed()

    def test_get_db_table(self):
        """
        Test get_db_table
        """
        assert zd_helpers.get_db_table('old_name') == 'old_name'

    def test_get_db_column(self):
        """
        Test get_db_column
        """
        assert zd_helpers.get_db_column('old_name') == 'old_name'

    def test_get_unique_together(self):
        """
        Test get_unique_together
        """
        assert zd_helpers.get_unique_together(('f1', 'f2')) is None


@pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                    reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
class TestZDHelpersWithOrgs(SimpleTestCase):
    """
    Test ZDHelpers when TAHOE_SITES_USE_ORGS_MODELS flag is On
    """
    def test_should_site_use_org_models(self):
        """
        Test should_site_use_org_models
        """
        assert not zd_helpers.should_site_use_org_models()

    def test_get_meta_managed(self):
        """
        Test get_meta_managed
        """
        assert zd_helpers.get_meta_managed()

    def test_get_db_table(self):
        """
        Test get_db_table
        """
        assert zd_helpers.get_db_table('old_name') is None

    def test_get_db_column(self):
        """
        Test get_db_column
        """
        assert zd_helpers.get_db_column('old_name') is None

    def test_get_unique_together(self):
        """
        Test get_unique_together
        """
        assert zd_helpers.get_unique_together(('f1', 'f2')) == ('f1', 'f2')
