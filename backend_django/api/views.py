# from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# from django.db import connection
# from sqlparse import format
# from pygments import highlight
# from pygments.formatters import TerminalFormatter
# from pygments.lexers import SqlLexer
from .serializers import StockSerializer, HistoricalSerializer
from .models import Stock, Historical

# Create your views here.


class StockViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing stock data.
    """

    queryset = Stock.objects.isActive()
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        queryset = Stock.objects.filter(slug=slug.upper())
        serializer = StockSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(responses=StockSerializer)
    def list(self, request):
        serializer = StockSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path=r"1/(?P<symbol>\w+)")
    def list_stock_by_symbol(self, request, symbol=None):
        queryset = Stock.objects.filter(symbol=symbol.upper())
        serializer = StockSerializer(queryset, many=True)
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

    @action(methods=["get"], detail=False, url_path=r"stock/(?P<symbol>\w+)/All")
    def list_historical_by_symbol(self, request, symbol=None):
        queryset = Historical.objects.filter(stock__symbol=symbol)

        serializer = HistoricalSerializer(queryset, many=True)

        return Response(serializer.data)
