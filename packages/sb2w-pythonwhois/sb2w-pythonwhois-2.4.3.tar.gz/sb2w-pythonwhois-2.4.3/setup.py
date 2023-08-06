from setuptools import setup

setup(name='sb2w-pythonwhois',
      version='2.4.3',
      description='Temporary Fork - the original project is `http://cryto.net/pythonwhois` Module for retrieving and parsing the WHOIS data for a domain. Supports most domains. No dependencies.',
      author='siteblindado',
      author_email='account.dev@siteblindado.com.br',
      url='https://github.com/siteblindado/python-whois',
      packages=['pythonwhois'],
      package_dir={"pythonwhois":"pythonwhois"},
      package_data={"pythonwhois":["*.dat"]},
      install_requires=['argparse'],
      provides=['pythonwhois'],
      scripts=["pwhois"],
      license="WTFPL"
     )
