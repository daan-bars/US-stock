from rest_framework import serializers
from .models import Stock, Historical


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["symbol", "name"]


class HistoricalSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = Historical
        fields = "__all__"
