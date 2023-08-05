from setuptools import setup

setup(name='tfnets',
      version='0.6.0',
      description='A library of common models implemented in tensorflow',
      author='Huy Nguyen',
      author_email='huy@huyng.com',
      packages=['tfnets', "tfnets.vgg16"],
      zip_safe=False,
      url="https://github.com/huyng/tfnets")

# to distribute run:
# python setup.py register sdist  upload
