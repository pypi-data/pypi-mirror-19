from distutils.core import setup
setup(
  name = 'ipdns',
  packages = ['ipdns', 'twisted.plugins'],
  version = '0.1.3',
  description = 'Stateless dns server serving ip addresses based on parsing the domain',
  author = 'Geert Audenaert',
  author_email = 'geert@greenitglobe.com',
  url = 'https://github.com/0-complexity/ipdns',
  download_url = 'https://github.com/0-complexity/ipdns/tarball/0.1',
  keywords = ['ip', 'dns', 'twisted'],
  classifiers = [],
  install_requires=['twisted', 'netaddr'],
)
