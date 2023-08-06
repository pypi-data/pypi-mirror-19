from setuptools import setup, find_packages

setup(
    name='wsssimpletest',
    version='0.0.1',
    keywords=('simple', 'test'),
    description='just a simple test',
    license='MIT License',
    install_requires=['simplejson>=1.1'],

    author='yjx',
    author_email='not@all.com',

    packages=find_packages(),
    platforms='any',
)