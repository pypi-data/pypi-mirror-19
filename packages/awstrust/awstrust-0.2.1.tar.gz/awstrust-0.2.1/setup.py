from setuptools import setup

setup(name='awstrust',
      packages=['awstrust'],
      version='0.2.1',
      description='Library for verifying AWS Instance Identity Documents',
      url='https://github.com/heph/awstrust',
      author='Stephen H. Adams',
      author_email='steve@steveadams.io',
      license='Apache License 2.0',
      install_requires=['M2Crypto'],
      zip_safe=True
     )
