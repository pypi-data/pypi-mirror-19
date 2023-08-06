from setuptools import setup

setup(
        name='yamlfmt',
        description='Opinionated yaml formmater based on ruamel.yaml',
        url='https://github.com/mmlb/yamlfmt',
        author='Manuel Mendez',
        author_email='mmendez534@gmail.com',
        version='0.1',
        scripts='yamlfmt',
        license='MPL 2.0',
        install_requires=[ 'ruamel.yaml'],
)
