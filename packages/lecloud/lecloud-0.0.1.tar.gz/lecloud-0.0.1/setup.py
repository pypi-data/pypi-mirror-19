from setuptools import find_packages, setup
from lecloud import __version__


setup(name="lecloud",
      version=__version__,
      description="Lecloud SDK python version",
      author="lecloud@gmail.com",
      url="http://lecloud.com",
      license="MIT",
      install_requires=[
          'tox==2.3.1',
          'flake8==2.5.4',
          'nose==1.3.7',
          'mock==2.0.0',
          'requests==2.10.0',
      ],
      packages=find_packages())
