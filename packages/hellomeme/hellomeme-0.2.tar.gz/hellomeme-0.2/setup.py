from setuptools import setup, find_packages

setup(name='hellomeme',
      version=0.02,
      description='Python package example',
      url='http://mywebsite',
      author='myname',
      author_email='tuora@students.wwu.edu',
      license='none',
      packages=find_packages(), # or list of packages path from this directory
      zip_safe=False,
      install_requires=[],
      classifiers=['Programming Language :: Python'],
      keywords=['Package Distribution'])
