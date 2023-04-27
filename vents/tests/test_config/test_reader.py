import os

from unittest import TestCase

from vents.settings import VENTS_CONFIG


class TestReader(TestCase):
    def test_get_from_env(self):
        assert VENTS_CONFIG.get_from_env(keys=None) is None
        assert VENTS_CONFIG.get_from_env(keys=[]) is None
        assert VENTS_CONFIG.get_from_env(keys="some_random_text_foo_000") is None

        os.environ["some_random_text_foo_000"] = "a"

        assert VENTS_CONFIG.get_from_env(["some_random_text_foo_000"]) == "a"

        del os.environ["some_random_text_foo_000"]

        os.environ["VENTS_some_random_text_foo_000"] = "a"

        assert VENTS_CONFIG.get_from_env(["some_random_text_foo_000"]) == "a"

        del os.environ["VENTS_some_random_text_foo_000"]
