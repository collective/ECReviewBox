from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='Products.ECReviewBox',
      version=version,
      description="The review box component of the eduComponents project.",
      long_description=open("README.txt").read() + "\n" +
                       #open(os.path.join("docs", "HISTORY.txt")).read()
                       '',
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Michael Piotrowski',
      author_email='mxp@dynalabs.de',
      url='http://plone.org/products/ecreviewbox',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.ECAssignmentBox',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )