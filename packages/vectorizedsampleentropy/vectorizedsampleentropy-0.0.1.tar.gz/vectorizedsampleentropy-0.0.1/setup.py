from setuptools import setup

setup(
    name = 'vectorizedsampleentropy',
    packages = ['vectorizedsampleentropy'],
    version = '0.0.1',
    description = "Vectorized versions of sample entropy (SampEn) and approximate entropy (ApEn)",
    author = 'Kira Huselius Gylling',
    author_email = 'kira.gylling@gmail.com',
    url = 'https://github.com/kirahg/vectorized-sample-entropy',
    download_url = 'https://github.com/kirahg/vectorized-sample-entropy/tarball/0.0.1',
    install_requires = ['numpy>=1.11.2'],
    license = 'GPL 3.0',
    keywords = ['entropy', 'data', 'statistics', 'time series'],
    classifiers = [],
)
