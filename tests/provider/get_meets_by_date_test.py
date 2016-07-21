from datetime import datetime

import cache_requests
from lxml import html
import punters_client
import pytest
import racing_data
import redis
import requests


@pytest.fixture(scope='module')
def meets():

    date = datetime(2016, 2, 1)

    http_client = None
    try:
        http_client = cache_requests.Session(connection=redis.fromurl('redis://localhost:6379/racing_data_test'))
    except BaseException:
        try:
            http_client = cache_requests.Session()
        except BaseException:
            http_client = requests.Session()

    html_parser = html.fromstring

    scraper = punters_client.Scraper(http_client, html_parser)

    provider = racing_data.Provider(scraper)

    return provider.get_meets_by_date(date)


def test_count(meets):
    """The get_meets_by_date method should return the expected number of meets"""

    assert len(meets) == 2


def test_types(meets):
    """The get_meets_by_date method should return a list of Meet objects"""

    assert isinstance(meets, list)
    for meet in meets:
        assert isinstance(meet, racing_data.Meet)
