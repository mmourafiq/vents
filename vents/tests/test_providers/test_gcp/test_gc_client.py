import mock

from unittest import TestCase

from vents.providers.gcp.base import get_gc_credentials
from vents.settings import VENTS_CONFIG

GCS_MODULE = "vents.providers.gcp.base.{}"


class TestGCClient(TestCase):
    @mock.patch(GCS_MODULE.format("google.auth.default"))
    def test_get_default_gc_credentials(self, default_auth):
        default_auth.return_value = None, None
        credentials = get_gc_credentials()
        assert default_auth.call_count == 1
        assert credentials is None

    @mock.patch(GCS_MODULE.format("Credentials.from_service_account_file"))
    def test_get_key_path_gc_credentials(self, service_account):
        with self.assertRaises(VENTS_CONFIG.exception):
            get_gc_credentials(key_path="key_path")

        service_account.return_value = None
        credentials = get_gc_credentials(key_path="key_path.json")
        assert service_account.call_count == 1
        assert credentials is None

    @mock.patch(GCS_MODULE.format("Credentials.from_service_account_info"))
    def test_get_keyfile_dict_gc_credentials(self, service_account):
        with self.assertRaises(VENTS_CONFIG.exception):
            get_gc_credentials(keyfile_dict="keyfile_dict")

        service_account.return_value = None

        credentials = get_gc_credentials(keyfile_dict={"private_key": "key"})
        assert service_account.call_count == 1
        assert credentials is None

        credentials = get_gc_credentials(keyfile_dict='{"private_key": "private_key"}')
        assert service_account.call_count == 2
        assert credentials is None
