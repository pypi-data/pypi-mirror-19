from setuptools import setup

setup(name='eveapimongo',
      version='0.1',
      description='EvE-API and MongoDB Wrappers',
      # url='http://github.com/storborg/funniest',
      author='Michael Bahr',
      # author_email='flyingcircus@example.com',
      license='MIT',
      packages=['eveapimongo'],
      install_requires=[
            'pymongo',
            'requests'
      ],
      zip_safe=False)
