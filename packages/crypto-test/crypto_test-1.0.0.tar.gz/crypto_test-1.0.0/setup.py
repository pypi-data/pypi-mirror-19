
# Always prefer setuptools over distutils
from setuptools import setup


setup(name='crypto_test',
      version='1.0.0',
      description='The easiest way to integrate Crypto Wallet Api Functions in your applications. Sign up at Cryptowallet.com for your API key.',
      url='',
      author='Pravin J',
      author_email='pravintest3@gmail.com',
      license='ISC',
      packages=['crypto_test'],
      install_requires=[
          'requests',
          'pycrypto',
          'ecdsa',
          'six',
          'base58'
      ],
      zip_safe=False)

# for packages not on pypi
# dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0']
