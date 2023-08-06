from setuptools import setup

setup(
        name='yamlfmt',
        description='Opinionated yaml formatter based on ruamel.yaml',
        url='https://github.com/mmlb/yamlfmt',
        author='Manuel Mendez',
        author_email='mmendez534@gmail.com',
        version='0.1.2',
        scripts=['yamlfmt'],
        license='MPL',
        install_requires=['ruamel.yaml']
)
