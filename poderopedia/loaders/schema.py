import logging

from poderopedia.core import grano, NotFound
from poderopedia.loaders.util import read_yaml


log = logging.getLogger(__name__)


def load_schema(schema_data):
    name = schema_data.get('name')
    try:
        schema = grano.schemata.by_name(name)
        schema._data = schema_data
        schema.save()
        log.info('Updated schema: %s', schema.label)
    except NotFound:
        schema = grano.schemata.create(schema_data)
        log.info('Created schema: %s', schema.label)


def load_schemata():
    mapping = {}
    data = read_yaml('schemata.yaml')
    for schema in data:
        load_schema(schema)
        mapping[schema.get('label')] = schema.get('name')
    return mapping
