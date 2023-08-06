from setuptools import setup

setup(name='pycfslib',
      version='0.2',
      description='Library to read, write and create CFS file and stream.',
      url='http://github.com/amiyapatanaik/pycfslib',
      author='Amiya Patanaik',
      author_email='amiya@duke-nus.edu.sg',
      license='GPL',
      packages=['pycfslib'],
      install_requires=[
          'numpy',
          'scipy',
      ],
      zip_safe=False)