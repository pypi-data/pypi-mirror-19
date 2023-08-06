from setuptools import setup

setup(name='clicker-server',
      version='0.1',
      description='Clicker Server',
      url='http://github.com/ftes/clicker',
      author='Fredrik Teschke',
      author_email='f@ftes.de',
      packages=['server'],
      install_requires=[
          'markdown',
          'python-socketio',
      ],
      zip_safe=False)
