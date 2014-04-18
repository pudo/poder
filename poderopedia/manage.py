from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from poderopedia.core import assets
from poderopedia.web import app
from poderopedia.generators import freezer
from poderopedia.loaders.podernx import import_poder

manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))


@manager.command
def load():
    """ Load all the datas. """
    import_poder()


@manager.command
def freeze():
    """ Freeze the entire site to static HTML. """
    app.config['DEBUG'] = False
    app.config['ASSETS_DEBUG'] = False
    freezer.freeze()


@manager.command
def run(port):
    app.run(host='0.0.0.0', port=int(port), debug=app.debug)


if __name__ == "__main__":
    manager.run()
