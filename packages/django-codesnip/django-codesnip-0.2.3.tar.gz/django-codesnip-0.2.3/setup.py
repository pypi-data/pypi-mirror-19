import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-codesnip',
    install_requires=['pygments'],
    version='0.2.3',
    packages=find_packages(),
    include_package_data=True,
    test_suite='runtests.runtests',
    license='LGPLv3',
    description='A Django app to store code snippets with syntax highlighting '
                'utilizing pygments.',
    long_description=README,
    url='https://github.com/vacuus/django-codesnip',
    author='Alejandro Angulo',
    author_email='aab.j13@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
