import os
from pprint import pprint
import json
import logging

from granoclient import Grano, NotFound
from granoclient.loader import Loader

from poderopedia.core import grano
from poderopedia.loaders.schema import load_schemata


log = logging.getLogger('poderimport')
SOURCE_URL = 'http://poderopedia.org'


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
    mappping = load_schemata()

    ld = Loader(grano, source_url=SOURCE_URL)
    data = read_data()
    entities = import_nodes(ld, data['nodes'])
    import_links(ld, data['links'], mapping, entities)


if __name__ == '__main__':
    import_poder()
