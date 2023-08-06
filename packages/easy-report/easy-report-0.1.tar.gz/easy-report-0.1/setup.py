import os
from setuptools import find_packages, setup
from pip.req import parse_requirements


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session='hack')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='easy-report',
    version='0.1',
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    license='MIT',
    description='Ease report for devs',
    long_description=README,
    url='https://github.com/MrLucasCardoso/easy_report',
    author='Lucas Cardoso',
    author_email='mr.lucascardoso@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
