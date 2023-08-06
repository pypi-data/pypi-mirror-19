try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='cipka',
    version='0.0.1',
    packages=['cipka'],
    license='MIT',
    url='https://github.com/PiotrDabkowski',
    author='Piotr Dabkowski',
    author_email='piodrus@gmail.com',
)
