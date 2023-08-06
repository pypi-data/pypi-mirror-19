"""Setup information for the Skytap API package."""
from setuptools import find_packages
from setuptools import setup

setup(
    name='skytap',
    packages=find_packages(),
    version='1.4.0',
    description='Skytap REST API access modules',
    author='Bill Wellington, Michael Knowles, and Caleb Hawkins',
    test_suite='nose.collector',
    author_email='bill@wellingtonnet.net',
    maintainer='Michael Knowles',
    maintainer_email='michael@mapledyne.com',
    license='MIT',
    install_requires=['requests', 'six'],
    scripts=['bin/skytap'],
    url='https://github.com/mapledyne/skytap',
    download_url='https://github.com/mapledyne/skytap/tarball/v1.4.0',
    keywords=['skytap', 'cloud', 'client', 'rest', 'api', 'development'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Internet"
    ]
)
