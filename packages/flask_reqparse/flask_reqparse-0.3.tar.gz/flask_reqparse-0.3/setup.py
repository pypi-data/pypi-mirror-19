from distutils.core import setup
setup(
  name = 'flask_reqparse',
  package = ['flask_reqparse'],
  version = '0.3',
  description = 'A requestparser for flask apps',
  author = 'Smit Thakkar',
  author_email = 'smitthakkar96@gmail.com',
  url = 'https://github.com/smitthakkar96/flask_reqparse', # use the URL to the github repo
  keywords = ['flask_reqparse', 'request parsing flask', 'flask request parser'], # arbitrary keywords
  install_requires=['flask', 'six'],
  classifiers = [],
)