from setuptools import setup, find_packages
setup(name="syno", version="0.0.3",
      packages=['syno', 'syno.async'],
      requires=['aiohttp', 'asyncio', 'async_timeout'],
      url="http://github.com/bobuk/syno",
      author="Grigory Bakunov",
      author_email='thebobuk@ya.ru',
      description='Synology API wrapper with aiohttp/asyncio')
