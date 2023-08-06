# coding: utf-8

from distutils.core import setup


__version__ = '0.0.3'

short_description = 'Django client for beatle'

setup(
    name='django-beatle',
    packages=['django_beatle'],
    version=__version__,
    description=short_description,
    long_description=short_description,
    author='Alexander Zhebrak',
    author_email='fata2ex@gmail.com',
    license='MIT',
    url='https://github.com/zhebrak/django-beatle',
    keywords=['python', 'django', 'beatle', 'cron', 'http request'],
    include_package_data=True,
    classifiers=[],
)
