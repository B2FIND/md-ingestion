
import os
import pathlib

from mdingestion import walker

from .common import TESTDATA_DIR


def test_walk():
    my_walker = walker.Walker(TESTDATA_DIR)
    path = os.path.join('darus', 'raw')
    files = [f for f in my_walker.walk(path=path, ext='.xml')]
    assert len(files) == 2
    assert '02baec53-8e79-5611-981e-11df59b824e4.xml' in sorted(files)[0]


def test_filter_after_date():
    file = pathlib.Path(os.path.join(
        TESTDATA_DIR, 'envidat-datacite', 'raw', 'bbox_80e203d7-7c64-5c00-8d1f-a91d49b0fa16.xml'))
    assert walker.filter_after_date(file) is True
    assert walker.filter_after_date(file, date=walker.parse_date('2020-05-01')) is True
    assert walker.filter_after_date(file, date=walker.parse_date('2120-05-01')) is False
