from setuptools import setup
from setuptools import find_packages


setup(
    name='bittray',
    version='0.1.4',
    packages=find_packages(),
    author='Nicolas Kuttler',
    author_email='pypi@kuttler.eu',
    description='Bitcoin info in your systray',
    keywords='bitcoin systray',
    long_description=open('README.rst').read(),
    license='BSD',
    url='http://github.com/nkuttler/bittray',
    entry_points={
        'console_scripts': [
            'bittray = bittray.console_scripts:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'bitcoin-price-api',
        'Pillow',
        'pystray',
        'webcolors',
        # For bitcoind functionality
        'python-bitcoinrpc',
        'notify2',
    ],
    # zip_safe=True,
)
