from setuptools import setup

setup(name='autocharles',
      version='1.0',
      description='Script for automating the parsing of Charles XML sessions',
      url='http://github.com/mdiblasio/autocharles',
      author='Michael DiBlasio',
      author_email='mdiblasio@google.com',
      license='',
      scripts=['bin/autochares'],
      packages=['autocharles'],
      zip_safe=False)
