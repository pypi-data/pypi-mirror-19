from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='openfigi',
    version='0.0.1',
    description='A simple wrapper for openfigi.com',
    long_description=readme,
    author='Julian Wergieluk',
    author_email='julian@wergieluk.com',
    url='https://github.com/wergieluk/openfigi',
    license=license,
    packages=find_packages()
)
