from .base import Community
from ..service_types import SchemaType, ServiceType


class DarusDatacite(Community):
    NAME = 'tudatalib'
    IDENTIFIER = 'tudatalib'
    URL = 'https://tudatalib.ulb.tu-darmstadt.de/oai/openairedata'
    SCHEMA = SchemaType.DataCite
    SERVICE_TYPE = ServiceType.OAI
    OAI_METADATA_PREFIX = 'oai_datacite'
    OAI_SET = None

    def update(self, doc):
        doc.contact = 'tudata@tu-darmstadt.de'
