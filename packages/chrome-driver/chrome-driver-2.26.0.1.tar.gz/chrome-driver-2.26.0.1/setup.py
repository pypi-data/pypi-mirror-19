
import hashlib
import os
import tempfile
import urllib
import zipfile

from setuptools import setup
from setuptools.command.install import install


URL = ('https://chromedriver.storage.googleapis.com/2.26'
       '/chromedriver_linux64.zip')
ETAG = '3cdae483af1e54c6732abc9af875b9c1'


def download_and_extract():
  print 'Downloading %s' % URL
  tmp = tempfile.NamedTemporaryFile(delete=False)
  tmp.close()

  urllib.urlretrieve(URL, tmp.name)

  with open(tmp.name, 'rb') as f:
    actual_etag = hashlib.md5(f.read()).hexdigest()
    if actual_etag != ETAG:
      raise Exception(
          'The checksum (md5) of %s is not correct (expected=%s, actual=%s).'
          ' It is unsafe to use the downloaded zip.'
          % (URL, ETAG, actual_etag))

  if not os.path.exists('bin'):
    os.mkdir('bin')
  with zipfile.ZipFile(tmp.name, 'r') as z:
    z.extract('chromedriver', 'bin')


class _install(install):
  def run(self):
    download_and_extract()
    install.run(self)


setup(
    name='chrome-driver',
    version='2.26.0.1',
    description='Chromedriver for pip.',
    url='https://github.com/tanin47/chrome-driver-pip',
    author='Tanin Na Nakorn',
    license='BSD',
    scripts=['bin/chromedriver'],
    cmdclass={'install': _install},
    zip_safe=False
)
