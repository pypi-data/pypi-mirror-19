from setuptools import setup, find_packages

version = '0.1.2'

REQUIREMENTS = [
    'python-dateutil',
    'requests'
]

setup(
    name='python-shopify',
    version=version,
    packages=find_packages(),
    url='https://github.com/rochacbruno/python-shopify-api',
    license='LICENSE.txt',
    author='Bruno Rocha & Mark Sanders',
    author_email='rochacbruno@gmail.com',
    install_requires=REQUIREMENTS,
    description='Wrapper and parser modules for Shopify\'s API.',
    include_package_data=True
)
