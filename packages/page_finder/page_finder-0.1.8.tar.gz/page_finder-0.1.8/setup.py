from setuptools import setup
from setuptools.extension import Extension

setup(
    name='page_finder',
    version='0.1.8',
    url='https://github.com/scrapinghub/page_finder',
    author='page_finder developers',
    maintainer='Ruairi Fahy',
    maintainer_email='ruairi@scrapinghub.com',
    install_requires=['numpy'],
    packages=['page_finder'],
    ext_modules=[Extension("page_finder.edit_distance",
                 sources=["page_finder/edit_distance.c"])],
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
