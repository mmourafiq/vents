from unittest import TestCase

from clipped.utils.assertions import assert_equal_dict
from pydantic import ValidationError

from vents.connections.k8s_resource import K8sResource


class TestK8sResource(TestCase):
    def setUp(self):
        self.spec1 = K8sResource(name="test1", is_requested=True)
        self.spec2 = K8sResource(name="test2", is_requested=False)
        self.spec3 = K8sResource(
            name="test3",
            items=["item45"],
            mount_path="/some_path",
            is_requested=False,
        )
        super().setUp()

    def test_resource_config(self):
        config_dict = {"name": "foo"}
        config = K8sResource.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "mount_path": 213}
        with self.assertRaises(ValidationError):
            K8sResource.from_dict(config_dict)

        config_dict = {"name": "foo", "items": 213}
        with self.assertRaises(ValidationError):
            K8sResource.from_dict(config_dict)

        config_dict = {
            "name": "foo",
            "mountPath": "/foo/path",
            "items": ["item1", "item2"],
        }
        config = K8sResource.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "items": ["item1", "item2"]}
        config = K8sResource.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_claim_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            K8sResource.from_dict(config_dict)

        config_dict = {"name": "sdf"}
        K8sResource.from_dict(config_dict)

        config_dict = {"name": "sdf", "items": ["foo"], "mountPath": "/bar"}
        config = K8sResource.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_resource_config(self):
        config_dict = {"name": "foo"}
        config = K8sResource.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "mount_path": 213}
        with self.assertRaises(ValidationError):
            K8sResource.from_dict(config_dict)

        config_dict = {"name": "foo", "items": 213}
        with self.assertRaises(ValidationError):
            K8sResource.from_dict(config_dict)

        config_dict = {
            "name": "foo",
            "mountPath": "/foo/path",
            "items": ["item1", "item2"],
        }
        config = K8sResource.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "items": ["item1", "item2"]}
        config = K8sResource.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
