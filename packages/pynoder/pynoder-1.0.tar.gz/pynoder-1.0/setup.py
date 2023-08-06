from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pynoder',
      version='1.0',
      description='A Python and PyQt5 package for creating a node-based editor.',
      long_description=readme(),
      url='https://github.com/johnroper100/PyNoder',
      author='John Roper',
      author_email='johnroper100@gmail.com',
      license='GPL3.0',
      packages=['pynoder'],
      install_requires=['PyQt5',],
      zip_safe=False)