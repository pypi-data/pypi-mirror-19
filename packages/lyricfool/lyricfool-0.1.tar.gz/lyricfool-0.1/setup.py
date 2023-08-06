from setuptools import setup

setup(name='lyricfool',
      version='0.1',
      description='lyricfool',
      url='http://github.com/miciaiahparker/lyricfool',
      author='Micaiah Parker',
      author_email='me@micaiahparker.com',
      license='MIT',
      packages=['lyricfool'],
      install_requires=[
          'requests',
          'hug',
          'bs4',
          'requests',
          'beautifulsoup4',
          'lxml'
      ],
      entry_points={
          'console_scripts': ['lyricfool=lyricfool.app:main']
      })
