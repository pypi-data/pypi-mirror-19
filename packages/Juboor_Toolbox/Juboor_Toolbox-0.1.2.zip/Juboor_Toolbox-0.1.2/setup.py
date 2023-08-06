from setuptools import setup

setup(name='Juboor_Toolbox',
      version='0.1.2',
      description='This is a compilation of the tools that I use from day-to-day',
      url='http://github.com/Djuboor/Juboor_Toolbox',
      author='David Juboor',
      author_email='dnjuboor@gmail.com',
      license='MIT',
      packages=['Juboor_Toolbox'],
      zip_safe=False)

# In order to update metadata, and publish a new build in a single step:
#    python setup.py register sdist upload