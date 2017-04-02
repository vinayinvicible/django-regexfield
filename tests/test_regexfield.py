from __future__ import absolute_import, unicode_literals

from django.db import DataError, IntegrityError, connection

import pytest

from .models import Page

pytestmark = pytest.mark.django_db

MYSQL_REASON = 'MySQL parses check constraints but are ignored by all engines'


def test_match():
    Page.objects.create(url='^/[A-Z]*/$')
    assert Page.objects.filter(url__match='/PATH/')
    assert not Page.objects.filter(url__match='/path/')


def test_imatch():
    Page.objects.create(url='^/[a-z]*/$')
    assert Page.objects.filter(url__imatch='/path/')
    assert Page.objects.filter(url__imatch='/PATH/')


@pytest.mark.skipif('connection.vendor == "mysql"', reason=MYSQL_REASON)
@pytest.mark.parametrize('regex', ('', '.*', '.?', '[\w]*', '[\w]?'))
def test_empty_regex(regex):
    with pytest.raises(IntegrityError):
        Page.objects.create(url=regex)


@pytest.mark.skipif('connection.vendor == "mysql"', reason=MYSQL_REASON)
def test_invalid_regex():
    exception = IntegrityError if connection.vendor == 'sqlite' else DataError
    with pytest.raises(exception):
        Page.objects.create(url='(?P<match>.*)')
