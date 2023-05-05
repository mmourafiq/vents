from unittest import TestCase

from vents.connections import ConnectionCatalog, ConnectionResource
from vents.connections.connection import Connection
from vents.connections.connection_schema import BucketConnection
from vents.providers.kinds import ProviderKind


class TestConnectionCatalog(TestCase):
    def setUp(self):
        super().setUp()
        self.secret1 = ConnectionResource(
            name="non_mount_test1",
            items=["item1", "item2"],
        )
        self.secret2 = ConnectionResource(
            name="non_mount_test2",
        )
        self.secret3 = ConnectionResource(
            name="non_mount_test3",
            items=["item1", "item2"],
        )
        self.config1 = ConnectionResource(
            name="non_mount_test1",
            items=["item1", "item2"],
        )
        self.s3_store = Connection(
            name="s3_store",
            kind=ProviderKind.S3,
            tags=["test", "foo"],
            secret=self.secret1,
            schema_=BucketConnection(bucket="s3//:foo"),
        )
        self.gcs_store = Connection(
            name="gcs_store",
            kind=ProviderKind.GCS,
            tags=["test"],
            secret=self.secret2,
            config_map=self.config1,
            schema_=BucketConnection(bucket="gs//:foo"),
        )
        self.az_store = Connection(
            name="az_store",
            kind=ProviderKind.WASB,
            secret=self.secret3,
            schema_=BucketConnection(bucket="wasbs://x@y.blob.core.windows.net"),
        )

    def test_empty_catalog(self):
        catalog = ConnectionCatalog()
        assert catalog.connections is None
        assert catalog.all_connections == []
        assert catalog.connections_by_names == {}
        assert catalog.secrets is None
        assert catalog.config_maps is None
        assert catalog.connections_by_names.get("test") is None

        catalog = ConnectionCatalog(connections=[])
        assert catalog.connections == []
        assert catalog._all_connections == []
        assert catalog._connections_by_names == {}
        assert catalog.secrets is None
        assert catalog.config_maps is None
        assert catalog.connections_by_names.get("test") is None

    def test_set_all_connections(self):
        catalog = ConnectionCatalog(connections=[self.s3_store, self.gcs_store])
        assert catalog.connections == [self.s3_store, self.gcs_store]
        assert catalog.all_connections == [self.s3_store, self.gcs_store]
        assert catalog.connections_by_names == {
            self.s3_store.name: self.s3_store,
            self.gcs_store.name: self.gcs_store,
        }
        assert catalog.secrets == [self.secret1, self.secret2]
        assert catalog.config_maps == [self.config1]
        assert catalog.connections_by_names.get("test") is None
        assert catalog.connections_by_names.get("az_store") is None
        assert catalog.connections_by_names.get("s3_store") == self.s3_store
        assert catalog.connections_by_names.get("gcs_store") == self.gcs_store

        # Reset catalog
        catalog.connections = [self.az_store]
        # set_all_connections is not called automatically
        assert catalog.connections == [self.az_store]
        assert catalog.all_connections == [self.s3_store, self.gcs_store]
        assert catalog.connections_by_names == {
            self.s3_store.name: self.s3_store,
            self.gcs_store.name: self.gcs_store,
        }
        assert catalog.secrets == [self.secret1, self.secret2]
        assert catalog.config_maps == [self.config1]
        assert catalog.connections_by_names.get("test") is None
        assert catalog.connections_by_names.get("az_store") is None
        assert catalog.connections_by_names.get("s3_store") == self.s3_store
        assert catalog.connections_by_names.get("gcs_store") == self.gcs_store
        # Calling set_all_connections manually
        catalog.set_all_connections()
        assert catalog.connections == [self.az_store]
        assert catalog.all_connections == [self.az_store]
        assert catalog.connections_by_names == {self.az_store.name: self.az_store}
        assert catalog.secrets == [self.secret3]
        assert catalog.config_maps == []
        assert catalog.connections_by_names.get("test") is None
        assert catalog.connections_by_names.get("s3_store") is None
        assert catalog.connections_by_names.get("gcs_store") is None
        assert catalog.connections_by_names.get("az_store") == self.az_store
