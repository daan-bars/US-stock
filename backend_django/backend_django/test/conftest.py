from pytest_factoryboy import register

from backend_django.test.factories import StockFactory, HistoricalFactory

register(StockFactory)
register(HistoricalFactory)
