import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from backend_django.test.factories import (
    StockFactory,
    HistoricalFactory,
    BackTestingFactory,
    StrategyStepsFactory,
)

register(StockFactory)
register(HistoricalFactory)
register(BackTestingFactory)
register(StrategyStepsFactory)


@pytest.fixture
def api_client():
    return APIClient
