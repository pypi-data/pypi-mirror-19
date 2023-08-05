"""Set functional dev tools"""
from pip.req import parse_requirements
from setuptools import setup, find_packages


dependencies = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in dependencies]
setup(
    name='pyfunk',
    version='1.0.0',
    url='https://github.com/danceasarxx/pyfunk.git',
    author='Arewa Olakunle',
    author_email='arewa.olakunle@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=reqs,
    long_description=open("README.md").read()
)
