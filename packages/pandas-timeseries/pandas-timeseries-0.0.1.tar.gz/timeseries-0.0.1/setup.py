from setuptools import setup

from timeseries import __version__

setup(
    author='Peter Brooks',
    author_email='peter@sealevelresearch.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering',
    ],
    description='Time series for dealing with window/point data sources, '
                'which has interpolation midful of gaps',
    install_requires=['pandas==0.19.1'],
    name='pandas-timeseries',
    packages=['timeseries'],
    url='https://github.com/sealevelresearch/timeseries',
    license='MIT',
    version=__version__,
    zip_safe=False,
)
