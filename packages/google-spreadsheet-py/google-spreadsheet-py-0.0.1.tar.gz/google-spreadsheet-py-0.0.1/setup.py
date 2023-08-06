from setuptools import setup, find_packages


version = '0.0.1'


setup(name='google-spreadsheet-py',
      version=version,
      description="A simple Python wrapper for the Google Spreadsheets API",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
          "Topic :: Utilities",
          "License :: OSI Approved :: BSD License",
          ],
      keywords='google, docs, spreadsheets, api',
      author='Ratson',
      author_email='contact@ratson.name',
      url='https://github.com/ratson/google-spreadsheet-py',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=["gdata"],
)
