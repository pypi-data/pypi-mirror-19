from setuptools import setup

setup(
  name='django-prerenderio',
  version='17.1.1',
  license='MIT',
  description="Django middleware to render Single Page Applications via prerender.io",
  
  author="Paul Bailey",
  author_email="paul.m.bailey@gmail.com",
  url="https://github.com/pizzapanther/django-prerenderio",
  
  package_dir={'django_prerenderio': 'src'},
  packages=['django_prerenderio'],
  
  install_requires=['requests'],
)
