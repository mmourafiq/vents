from unittest import TestCase

from vents.connections import ConnectionResource
from vents.connections.connection import Connection
from vents.connections.connection_schema import (
    BucketConnection,
    ClaimConnection,
    HostPathConnection,
)
from vents.providers.kinds import ProviderKind


class TestConnection(TestCase):
    def setUp(self):
        super().setUp()
        self.s3_store = Connection(
            name="test",
            kind=ProviderKind.S3,
            tags=["test", "foo"],
            schema_=BucketConnection(bucket="s3//:foo"),
        )
        self.gcs_store = Connection(
            name="test",
            kind=ProviderKind.GCS,
            tags=["test"],
            schema_=BucketConnection(bucket="gs//:foo"),
        )
        self.az_store = Connection(
            name="test",
            kind=ProviderKind.WASB,
            schema_=BucketConnection(bucket="wasbs://x@y.blob.core.windows.net"),
        )
        self.claim_store = Connection(
            name="test",
            kind=ProviderKind.VOLUME_CLAIM,
            schema_=ClaimConnection(
                volume_claim="test", mount_path="/tmp", read_only=True
            ),
        )
        self.host_path_store = Connection(
            name="test",
            kind=ProviderKind.HOST_PATH,
            schema_=HostPathConnection(
                host_path="/tmp", mount_path="/tmp", read_only=True
            ),
        )

        self.custom_connection1 = Connection(
            name="db",
            kind=ProviderKind.POSTGRES,
        )

        self.custom_connection2 = Connection(
            name="ssh",
            kind=ProviderKind.SSH,
            schema_=dict(key1="val1", key2="val2"),
        )

    def test_store_path(self):
        assert self.s3_store.store_path == self.s3_store.schema_.bucket
        assert self.s3_store.tags == ["test", "foo"]
        assert self.gcs_store.store_path == self.gcs_store.schema_.bucket
        assert self.gcs_store.tags == ["test"]
        assert self.az_store.store_path == "x"
        assert self.az_store.tags is None
        assert self.claim_store.store_path == self.claim_store.schema_.mount_path
        assert self.claim_store.tags is None
        assert self.host_path_store.store_path == self.claim_store.schema_.mount_path
        assert self.host_path_store.tags is None

    def test_is_bucket(self):
        assert self.s3_store.is_bucket is True
        assert self.s3_store.is_s3 is True
        assert self.s3_store.is_gcs is False

        assert self.gcs_store.is_bucket is True
        assert self.gcs_store.is_gcs is True
        assert self.gcs_store.is_s3 is False

        assert self.az_store.is_bucket is True
        assert self.az_store.is_wasb is True
        assert self.az_store.is_s3 is False
        assert self.az_store.is_gcs is False

        assert self.claim_store.is_bucket is False
        assert self.claim_store.is_s3 is False

        assert self.host_path_store.is_bucket is False
        assert self.host_path_store.is_s3 is False

    @staticmethod
    def assert_from_model(spec: Connection):
        result = Connection.from_model(model=spec)

        assert result.name == spec.name
        assert result.kind == spec.kind
        if spec.schema_ is None:
            assert result.schema_ == spec.schema_
        elif isinstance(spec.schema_, dict):
            assert result.schema_ == spec.schema_
        else:
            value_dict = spec.schema_.to_dict()
            result_dict = result.schema_.to_dict()
            assert value_dict.keys() == result_dict.keys()
            for k in result_dict.keys():
                assert value_dict[k] == result_dict[k]
        assert result.secret == spec.secret

    def test_get_from_model_s(self):
        self.assert_from_model(self.s3_store)
        self.assert_from_model(self.gcs_store)
        self.assert_from_model(self.az_store)
        self.assert_from_model(self.claim_store)
        self.assert_from_model(self.host_path_store)
        assert self.custom_connection1.schema_ is None
        self.assert_from_model(self.custom_connection1)
        assert self.custom_connection2.schema_ == {"key1": "val1", "key2": "val2"}
        self.assert_from_model(self.custom_connection2)


class TestMainSecrets(TestCase):
    def setUp(self):
        # Secrets
        self.resource1 = ConnectionResource(
            name="non_mount_test1",
            items=["item1", "item2"],
            is_requested=False,
        )
        self.resource2 = ConnectionResource(
            name="non_mount_test2",
            is_requested=False,
        )
        self.resource3 = ConnectionResource(
            name="non_mount_test3",
            items=["item1", "item2"],
            is_requested=True,
        )
        self.resource4 = ConnectionResource(
            name="non_mount_test4",
            is_requested=True,
        )
        self.resource5 = ConnectionResource(
            name="non_mount_test1",
            is_requested=True,
        )

        # Connections
        self.s3_store = Connection(
            name="test_s3",
            kind=ProviderKind.S3,
            schema_=BucketConnection(bucket="s3//:foo"),
            secret=self.resource1,
        )
        self.gcs_store = Connection(
            name="test_gcs",
            kind=ProviderKind.GCS,
            schema_=BucketConnection(bucket="gcs//:foo"),
            secret=self.resource2,
        )
        self.az_store = Connection(
            name="test_az",
            kind=ProviderKind.WASB,
            schema_=BucketConnection(bucket="wasb://x@y.blob.core.windows.net"),
            secret=self.resource3,
        )
        self.claim_store = Connection(
            name="test_claim",
            kind=ProviderKind.VOLUME_CLAIM,
            schema_=ClaimConnection(mount_path="/tmp", volume_claim="test"),
        )
        self.host_path_store = Connection(
            name="test_path",
            kind=ProviderKind.HOST_PATH,
            schema_=HostPathConnection(
                mount_path="/tmp", host_path="/tmp", read_only=True
            ),
        )

    def test_get_requested_secrets_non_values(self):
        assert (
            Connection.get_requested_resources(
                resources=None, connections=None, resource_key="secret"
            )
            == []
        )
        assert (
            Connection.get_requested_resources(
                resources=[], connections=[], resource_key="secret"
            )
            == []
        )
        assert (
            Connection.get_requested_resources(
                resources=[self.resource1, self.resource2],
                connections=[],
                resource_key="secret",
            )
            == []
        )
        assert (
            Connection.get_requested_resources(
                resources=[],
                connections=[self.host_path_store, self.claim_store],
                resource_key="secret",
            )
            == []
        )

    def test_get_requested_secrets_and_secrets(self):
        expected = Connection.get_requested_resources(
            resources=[], connections=[self.s3_store], resource_key="secret"
        )
        assert expected == [self.resource1]

        expected = Connection.get_requested_resources(
            resources=[self.resource2],
            connections=[self.s3_store],
            resource_key="secret",
        )
        assert expected == [self.resource1]

        expected = Connection.get_requested_resources(
            resources=[self.resource2],
            connections=[self.s3_store, self.gcs_store],
            resource_key="secret",
        )
        assert expected == [
            self.resource1,
            self.resource2,
        ]

        expected = Connection.get_requested_resources(
            resources=[self.resource1, self.resource2],
            connections=[self.s3_store, self.gcs_store, self.az_store],
            resource_key="secret",
        )
        assert expected == [
            self.resource1,
            self.resource2,
            self.resource3,
        ]

    def test_get_requested_secrets(self):
        expected = Connection.get_requested_resources(
            resources=[self.resource1],
            connections=[self.s3_store],
            resource_key="secret",
        )
        assert expected == [self.resource1]
        expected = Connection.get_requested_resources(
            resources=[self.resource1, self.resource3],
            connections=[self.s3_store],
            resource_key="secret",
        )
        assert expected == [
            self.resource3,
            self.resource1,
        ]
        expected = Connection.get_requested_resources(
            resources=[self.resource2, self.resource3, self.resource4],
            connections=[self.gcs_store],
            resource_key="secret",
        )
        assert expected == [
            self.resource3,
            self.resource4,
            self.resource2,
        ]
        expected = Connection.get_requested_resources(
            resources=[self.resource1, self.resource2],
            connections=[self.gcs_store],
            resource_key="secret",
        )
        assert expected == [self.resource2]
        expected = Connection.get_requested_resources(
            resources=[self.resource1, self.resource2],
            connections=[self.s3_store, self.gcs_store],
            resource_key="secret",
        )
        assert expected == [
            self.resource1,
            self.resource2,
        ]
        expected = Connection.get_requested_resources(
            resources=[self.resource1, self.resource2],
            connections=[
                self.s3_store,
                self.gcs_store,
                self.host_path_store,
                self.claim_store,
            ],
            resource_key="secret",
        )
        assert expected == [
            self.resource1,
            self.resource2,
        ]

        new_az_store = Connection(
            name="test_az",
            kind=ProviderKind.WASB,
            schema_=BucketConnection(bucket="wasb://x@y.blob.core.windows.net"),
            secret=self.resource1,
        )
        expected = Connection.get_requested_resources(
            resources=[self.resource1, self.resource2],
            connections=[
                self.s3_store,
                self.gcs_store,
                new_az_store,
                self.host_path_store,
                self.claim_store,
            ],
            resource_key="secret",
        )
        assert expected == [
            self.resource1,
            self.resource2,
        ]

        # Using a requested secret with same id
        expected = Connection.get_requested_resources(
            resources=[self.resource5, self.resource2],
            connections=[
                self.s3_store,
                self.gcs_store,
                new_az_store,
                self.host_path_store,
                self.claim_store,
            ],
            resource_key="secret",
        )
        assert expected == [
            self.resource5,
            self.resource2,
        ]
