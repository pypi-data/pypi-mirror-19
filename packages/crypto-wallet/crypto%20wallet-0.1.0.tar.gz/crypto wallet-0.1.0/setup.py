
# Always prefer setuptools over distutils
from setuptools import setup

import os

long_description = 'Crypto wallets are most secured digital wallets which are used to send and receive virtual currencies like bitcoin.'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(
      name='crypto wallet',
      version='0.1.0',
      description='The easiest way to integrate Crypto Wallet Api Functions in your applications. Sign up at Cryptowallet.com for your API key.',
      long_description=long_description,
      author='OsizTech',
      author_email='info@osiztechnologies.com',
      license='ISC',
      url = "http://www.osiztechnologies.com/",
      keywords = "CryptoWallet crypto_wallet bitcoin_api crypto wallet crypto_wallet_api",
      packages=['crypto_wallet'],
      install_requires=[
          'requests',
          'pycrypto',
          'ecdsa',
          'six',
          'base58'
      ],
      zip_safe=False
      )

# for packages not on pypi
# dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0']
