from poderopedia.core import freezer, grano


@freezer.register_generator
def entity():
    for entity in grano.entities:
        print 'Generate Entity: %s' % entity.id
        yield {'id': entity.id}

