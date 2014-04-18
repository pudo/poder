from setuptools import setup, find_packages


setup(
    name='poderopedia',
    version='2',
    description="",
    long_description=None,
    classifiers=[],
    keywords='',
    author='',
    author_email='',
    url='https://github.com/pudo/poder',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    zip_safe=False,
    install_requires=[
        "grano-client>=0.2",
        "Flask==0.10.1",
        "Flask-Assets==0.8",
        "Flask-Script==0.5.3",
        "PyYAML==3.10",
        "unicodecsv==0.9.4"
    ],
    tests_require=[],
    entry_points=\
    """ """,
)
