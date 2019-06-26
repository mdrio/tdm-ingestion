import datetime
import unittest
import uuid

from tdm_ingestion.ingesters.async_ingester import async_ingester_factory
from tdm_ingestion.ingestion import TimeSeries, ValueMeasure, \
    BasicIngester
from tests.dummies import DummyConsumer, DummyStorage, DummyConverter


class TestIngester(unittest.TestCase):

    def test_basic_ingester(self):
        storage = DummyStorage()
        ingester = BasicIngester(DummyConsumer(), storage, DummyConverter())
        ingester.process()
        self.assertEqual(len(storage.messages), 1)

    def test_async_ingester(self):
        storage = DummyStorage()
        ingester = async_ingester_factory([
            (DummyConsumer().poll, {}),
            (DummyConverter().convert, {}),
            (storage.write, {})]
        )
        ingester.process()
        self.assertEqual(len(storage.messages), 1)


class TestTimeSeries(unittest.TestCase):
    def test_to_dict(self):
        now = datetime.datetime.utcnow()
        sensorcode = uuid.uuid4()
        value = 100
        ts = TimeSeries(now, sensorcode, ValueMeasure(100))
        time_format = '%Y-%m-%dT%H:%M:%SZ'
        to_dict = ts.to_dict(time_format)
        self.assertEqual(to_dict['time'], now.strftime(time_format))
        self.assertEqual(to_dict['sensorcode'], str(sensorcode))
        self.assertEqual(to_dict['measure'], {'value': value})


if __name__ == '__main__':
    unittest.main()
