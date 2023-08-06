from setuptools import setup
from setuptools.extension import Extension
import sys

if sys.platform == 'win32':
    ext_modules = []
else:
    ext_modules = [Extension("page_finder.edit_distance",
                             sources=["page_finder/edit_distance.c"])]

setup(
    name='page_finder',
    version='0.1.9',
    url='https://github.com/scrapinghub/page_finder',
    author='page_finder developers',
    maintainer='Ruairi Fahy',
    maintainer_email='ruairi@scrapinghub.com',
    install_requires=['numpy'],
    packages=['page_finder'],
    ext_modules=ext_modules,
    license='MIT',
    keywords=['crawler', 'frontier', 'scrapy', 'web', 'requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
