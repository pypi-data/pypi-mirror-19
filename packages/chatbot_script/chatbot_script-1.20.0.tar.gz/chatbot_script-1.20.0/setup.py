from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
   long_description = f.read()
   
setup(name='chatbot_script',
      version='1.20.0',
      description='is a simple chatbot_script that uses simple matching ',
      long_description=long_description, 
      url='https://github.com/pypi/chatbot_script',license='MIT', classifiers=   
      ['Development Status :: 3 - Alpha','Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',],
      keywords='sample setuptools development',
      packages=find_packages(),
      install_requires=['peppercorn'],
      extras_require={
             'dev': ['check-manifest'],
             'test': ['coverage'],},
       package_data={
             'sample': ['package_data.dat'],},
       entry_points={
             'console_scripts': [
             'sample=sample:main',],},)