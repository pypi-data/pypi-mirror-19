from setuptools import setup

setup(name='mdiblasiofunniest',
      version='0.2',
      description='The funniest joke in the world',
      url='http://github.com/mdiblasio/funniest',
      author='Michael DiBlasio',
      author_email='mdiblasio@google.com',
      license='dibs',
      scripts=['bin/mdiblasiofunniest-joke'],
      packages=['mdiblasiofunniest'],
      zip_safe=False)
