import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

setup(
    name='geoshoplib',
    version='0.2.0',
    description='Python API to access geoshop services.',
    long_description=README + '\n\n' + CHANGES,
    license='GNU General Public License',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers", "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='Clemens Rudert',
    author_email='clemens.rudert@bl.ch',
    url='https://gitlab.com/gf-bl/geoshoplib',
    keywords='api geoshop infogrips soap xml',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'httplib2',
        'untangle'
    ]
)
