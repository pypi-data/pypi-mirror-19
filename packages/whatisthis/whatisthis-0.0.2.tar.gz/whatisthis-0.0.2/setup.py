from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='whatisthis',
      version='0.0.2',
      description='UI for manual image classification',
      long_description=readme(),
      url='http://github.com/Tom-Alexander/whatisthis',
      download_url = 'https://github.com/Tom-Alexander/whatisthis/tarball/0.0.1',
      author='Tom Alexander',
      author_email='me@tomalexander.co.nz',
      license='MIT',
      packages=['whatisthis'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'jinja2'
      ])
