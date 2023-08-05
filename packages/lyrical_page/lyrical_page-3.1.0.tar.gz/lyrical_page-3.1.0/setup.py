import os

from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='lyrical_page',
    version='3.1.0',
    description='Website content system based on a mashup of ideas from the Django contrib flatpage appp, joomla!, and many years of systems development..',
    author='Will LaShell',
    author_email='wlashell@lyrical.net',
    license='Apache Software License',
    long_description=README,
    url='http://www.lyrical.net/projects/lyrical_page/',
    packages=find_packages(),
    include_package_data=True,
    install_requires = ['Django>=1.10', 'django-grappelli>=2.9.1',
        'pytz>=2014.10'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django :: 1.10',
    ],
)
