from setuptools import find_packages, setup

setup(
    name='dataflow-wikipedia-pipeline',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'apache-beam[gcp]',
        'wikipedia-api==0.5.4',  # Specify the exact version or range you need
    ],
    description='Dataflow pipeline for processing Wikipedia data'
)
