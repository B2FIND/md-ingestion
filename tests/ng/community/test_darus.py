import os

from mdingestion.ng.community.darus import DarusDatacite

from tests.common import TESTDATA_DIR


def test_datacite():
    xmlfile = os.path.join(TESTDATA_DIR, 'darus-oai_datacite', 'SET_1', 'xml', '02baec53-8e79-5611-981e-11df59b824e4.xml')  # noqa
    reader = DarusDatacite()
    doc = reader.read(xmlfile, url='https://darus.uni-stuttgart.de/oai', community='darus', mdprefix='oai_datacite')
    assert 'Deep enzymology data' in doc.title[0]
    assert 'https://doi.org/10.18419/darus-629' == doc.doi
    assert 'https://darus.uni-stuttgart.de/oai?verb=GetRecord&metadataPrefix=oai_datacite&identifier=doi:10.18419/darus-629' == doc.metadata_access  # noqa
    assert 'Medicine Health and Life Sciences' in doc.keywords
    assert 'Medicine Health and Life Sciences' == doc.discipline
    assert 'Jeltsch, Albert (Universität Stuttgart)' in doc.contact
    assert 'application/pdf' in doc.format
    assert len(doc.format) == 2
    assert doc.open_access is True
    assert '2020-01-30T00:00:00Z' in doc.temporal_coverage_begin_date
