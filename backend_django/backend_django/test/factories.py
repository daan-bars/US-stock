import factory

from api.models import Stock, Historical


class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stock

    symbol = factory.Sequence(lambda n: f"symbol_{n}")
    name = factory.Sequence(lambda n: f"name_{n}")
    description = factory.Sequence(lambda n: f"description_{n}")
    sector = factory.Sequence(lambda n: f"sector_{n}")


class HistoricalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Historical

    stock = factory.SubFactory(StockFactory)
    date = factory.Sequence(lambda n: n)
    open = factory.Sequence(lambda n: n)
    high = factory.Sequence(lambda n: n)
    low = factory.Sequence(lambda n: n)
    close = factory.Sequence(lambda n: n)
    volume = factory.Sequence(lambda n: n)
