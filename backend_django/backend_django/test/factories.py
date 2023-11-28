import factory
from datetime import datetime, timedelta

from api.models import Stock, Historical, BackTesting, StrategySteps


class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stock

    symbol = factory.Sequence(lambda n: f"symbol_{n}")
    name = factory.Sequence(lambda n: f"name_{n}")
    description = factory.Sequence(lambda n: f"description_{n}")
    sector = factory.Sequence(lambda n: f"sector_{n}")
    slug = factory.Sequence(lambda n: f"slug_{n}")


class HistoricalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Historical

    stock = factory.SubFactory(StockFactory)
    date = factory.Sequence(
        lambda n: (datetime(2023, 1, 1) + timedelta(days=n)).strftime("%Y-%m-%d")
    )  # 2023-01-01 ~2023-XX-XX
    open = factory.Sequence(lambda n: round(n, 1))  # 100
    high = factory.Sequence(lambda n: round(n * 1.05, 1))  # 105
    low = factory.Sequence(lambda n: round(n * 0.95, 1))  # 95
    close = factory.Sequence(lambda n: round(n * 1.1, 1))  # 110
    volume = factory.Sequence(lambda n: n * 1000)  # 1000


class BackTestingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BackTesting

    stock = factory.SubFactory(StockFactory)
    name = factory.Sequence(lambda n: f"BackTesting_{n}")
    date = factory.Sequence(
        lambda n: (datetime(2023, 1, 1) + timedelta(days=n)).strftime("%Y-%m-%d")
    )  # 2023-01-01 ~2023-XX-XX
    strategyNumber = factory.Sequence(lambda n: n)
    is_active = True


class StrategyStepsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StrategySteps

    backTesting = factory.SubFactory(BackTestingFactory)
    step = factory.Sequence(lambda n: f"step_{n}")
    name = factory.Sequence(lambda n: f"name_{n}")
