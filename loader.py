import os
from pprint import pprint
import json
import yaml
import logging

from granoclient import Grano, NotFound
from granoclient.loader import Loader


log = logging.getLogger('poderimport')
SOURCE_URL = 'http://poderopedia.org'


def load_schema(grano, schema_data):
    name = schema_data.get('name')
    try:
        schema = grano.schemata.by_name(name)
        schema._data = schema_data
        schema.save()
        log.info('Updated schema: %s', schema.label)
    except NotFound:
        schema = grano.schemata.create(schema_data)
        log.info('Created schema: %s', schema.label)


def load_schemata(grano):
    mapping = {}
    with open('schemata.yaml', 'r') as fh:
        data = yaml.load(fh)
        for schema in data:
            load_schema(grano, schema)
            mapping[schema.get('label')] = schema.get('name')
    return mapping


def read_data():
    with open('data/exportPoderopedia.json', 'r') as fh:
        data = json.loads(json.load(fh))
        return data


def by_name(grano, name):
    q = grano.entities.query()
    q = q.filter('property-name', name)
    q = list(q.results)
    if len(q):
        return q[0]
    return None


def import_nodes(ld, nodes):
    entities = {}
    for num, node in enumerate(nodes):
        type_ = node.get('id')[0]
        #num = node.get('id')[1:]
        name = '%s (%s)' % (node.get('alias'), node.get('id'))
        print [name]
        entity = by_name(ld.project, name)
        if entity is None:
            schema = 'org' if type_ == 'O' else 'person'
            entity = ld.make_entity([schema, 'poderentity'])
            entity.set('name', name)
            entity.set('poderopedia_id', node.get('id'))
            entity.set('country', node.get('countryOfResidence'))
            entity.set('alias', node.get('alias'))
            if type_ == 'P':
                entity.set('short_bio', node.get('shortBio'))
            entity.save()
            #print entity.schemata, entity.properties
        entities[num] = entity
    return entities


def import_links(ld, links, mapping, entities):
    for link in links:
        schema, role = None, None
        for k, v in link.items():
            if k in ['source', 'target', 'weight', 'isPast']:
                continue
            schema = mapping[k]
            role = v
        rel = ld.make_relation(schema, entities[link.get('source')],
            entities[link.get('target')])
        rel.set('role', role)
        rel.save()


def import_poder():
    client = Grano(api_host=os.environ.get('GRANO_HOST'),
               api_key=os.environ.get('GRANO_APIKEY'))
    project_name = os.environ.get('GRANO_PROJECT')
    try:
        grano = client.get(project_name)
    except NotFound:
        data = {'slug': project_name, 'label': project_name}
        grano = client.projects.create(data)

    mappping = load_schemata(grano)

    ld = Loader(grano, source_url=SOURCE_URL)
    data = read_data()
    entities = import_nodes(ld, data['nodes'])
    import_links(ld, data['links'], mapping, entities)


if __name__ == '__main__':

    import_poder()
    import sys; sys.exit()
    data = read_data()
    #print data.keys()
    names = set()
    for node in data['nodes']:
        names.add(node.get('alias'))

    #print len(data['nodes']), len(names)
    #print data.keys()
    del data['nodes']
    rels = {}
    for link in data['links']:
        for k, v in link.items():
            if k in ['source', 'target', 'weight', 'isPast']:
                continue
            if k in rels:
                rels[k].add(v)
            else:
                rels[k] = set([v])
    #del data['links']
    #pprint(rels.keys())
    for rel in rels.keys():
        print rel
