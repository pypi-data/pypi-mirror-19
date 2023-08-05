from setuptools import setup, find_packages
import os

version = '1.0.0'

setup(name='collective.simplewiki',
      version=version,
      description="Simple wiki linking syntax support for Plone",
      long_description="%s\n%s" % (
          open("README.rst").read(),
          open("CHANGES.rst").read()
      ),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Framework :: Plone",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
      ],
      keywords='Plone wiki wicked',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='https://github.com/collective/collective.simplewiki',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api'
      ],
      extras_require={
          'test': [
              'plone.app.testing'
          ]
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
