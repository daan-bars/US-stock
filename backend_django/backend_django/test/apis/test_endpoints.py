# import factory
import pytest
import json

pytestmark = pytest.mark.django_db


class TestStockEndpoint:
    endPoint = "/api/Stock/"

    def test_stock_get(self, stock_factory, api_client):
        # Arrange
        stock_factory.create_batch(4)
        # Act
        response = api_client().get(self.endPoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    pass


class TestHistoricalEndpoint:
    endPoint = "/api/Historical/"

    def test_historical_get(self, historical_factory, api_client):
        # Arrange
        historical_factory.create_batch(100)
        # Act
        response = api_client().get(self.endPoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 100
        print(json.loads(response.content))

    pass
