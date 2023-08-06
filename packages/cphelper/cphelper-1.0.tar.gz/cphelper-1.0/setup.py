from distutils.core import setup

setup(
    name = 'cphelper',
    packages = ['cphelper'],
    version = '1.0',
    description = 'A API which',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/Stufinite/cphelper',
    download_url = 'https://github.com/Stufinite/cphelperarchive/v1.0.tar.gz',
    keywords = ['coursepickinghelper', 'timetable', 'campass'],
    classifiers = [],
    license='GNU3.0',
    install_requires=[
        'djangoApiDec==1.2',
        'pymongo==3.4.0',
    ],
    zip_safe=True
)
