from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cbpi4-PCA9535-GPIO',
      version='0.0.5',
      description='CraftBeerPi4 PCA9535 Actor Plugin',
      author='Waleed Badar',
      author_email='avollkopf@web.de',
      url='https://github.com/walidbadar/cbpi4-PCA9535-GPIO',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-PCA9535-GPIO': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-PCA9535-GPIO'],
      install_requires=[
      'smbus2',
      'pcf8574-io'
      ],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )
