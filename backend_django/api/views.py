# from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import StockSerializer, HistoricalSerializer
from .models import Stock, Historical

# Create your views here.


class StockViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing stock data.
    """

    queryset = Stock.objects.all()

    @extend_schema(responses=StockSerializer)
    def list(self, request):
        serializer = StockSerializer(self.queryset, many=True)
        return Response(serializer.data)


class HistoricalViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing historical data.
    """

    queryset = Historical.objects.all()

    @extend_schema(responses=HistoricalSerializer)
    def list(self, request):
        serializer = HistoricalSerializer(self.queryset, many=True)
        return Response(serializer.data)
