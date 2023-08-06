from setuptools import setup, find_packages


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = open('README.md').read()

setup(
    name='getpassecho',
    author='Kurt Spindler',
    author_email='kespindler@gmail.com',
    version='1.0',
    description='getpass with an echo char',
    long_description=long_description,
    packages=['getpassecho'],
)

