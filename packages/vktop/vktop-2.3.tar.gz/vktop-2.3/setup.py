from setuptools import setup
from vktop import __version__ as app_version

setup(
  name = 'vktop',
  packages=['vktop'],
  install_requires=['requests'],
  version = app_version,
  description = 'VK-Top is used for getting popular posts of any public available page at VK.com',
  author = 'Dmitry Yutkin',
  author_email = 'yutkinn@gmail.com',
  url = 'https://github.com/yutkin/VK-Top',
  download_url = 'https://github.com/yutkin/VK-Top/tarball/'+app_version,
  include_package_data=True,
  license='MIT',
  keywords = ['vk.com', 'vk', 'downloader', 'posts', 'social', 'networks', 'likes', 'reposts'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS',
    'Operating System :: Unix',
    'Operating System :: Microsoft',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2',
    'Topic :: Internet',
    'Topic :: Utilities'
  ],
  entry_points=dict(
    console_scripts=[
        'vktop=vktop.__main__:main'
    ]
  ),
)
