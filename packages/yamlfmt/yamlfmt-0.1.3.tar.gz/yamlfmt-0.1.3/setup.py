from setuptools import setup

setup(
        name='yamlfmt',
        description='Opinionated yaml formatter based on ruamel.yaml',
        long_description=open('README.md').read(),
        url='https://github.com/mmlb/yamlfmt',
        author='Manuel Mendez',
        author_email='mmendez534@gmail.com',
        version='0.1.3',
        scripts=['yamlfmt'],
        license='[MPLv2.0](https://mozilla.org/MPL/2.0/)',
        install_requires=['ruamel.yaml'],
        classifiers=[
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
            'Programming Language :: Python :: 3',
            'Topic :: Utilities',
        ],
        keywords='yaml format'
)
