from distutils.core import setup

setup(
    name = 'djangoApiDec',
    packages = ['djangoApiDec'],
    version = 'v1.2',
    description = 'Convenient python decorator usually used for building api',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/Stufinite/djangoApiDec',
    download_url = 'https://github.com/Stufinite/djangoApiDec/archive/v1.2.tar.gz',
    keywords = ['django', 'decorator', 'api'],
    classifiers = [],
    license='MIT',
    install_requires=[
        'django==1.10.3',
        'requests',
        'simplejson'
    ],
    zip_safe=True
)
