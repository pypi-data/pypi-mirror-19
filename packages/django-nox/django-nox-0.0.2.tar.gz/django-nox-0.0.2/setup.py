from setuptools import setup, find_packages
import os
import sys
import io

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


setup(name='django-nox',
      version='0.0.2',
      description='Statistics middleware and analysis tools for django',
      long_description=read('README.rst'),
      url='https://github.com/destino74/django-nox',
      author='destino74',
      author_email='ljf6670601@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests', 'config']),
      # packages=['django_nox', 'django_nox.migrations', 'django_nox.management', 'django_nox.management.commands'],
      install_requires=[
            'texttable',
#            'markdown',
      ],
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
      ],
      zip_safe=False)
