import types
from unittest import TestCase

from data._extraction._data_extractor import ExtractorFactory

DATAFOLDER = "/run/media/sebsch/ArgoData/201707-ArgoData/aoml/"


class TestExtractorFactory(TestCase):
    def test_dataset(self):
        ef = ExtractorFactory(DATAFOLDER)
        ds = ef.get_data_sets()
        self.assertIsNotNone(ds)

    def test_dataset_return_type(self):
        ef = ExtractorFactory(DATAFOLDER)
        ds = ef.get_data_sets()
        self.assertTrue(isinstance(ds, types.GeneratorType))
