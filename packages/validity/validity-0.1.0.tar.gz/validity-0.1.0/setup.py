from setuptools import setup

setup(name='validity',
      version='0.1.0',
      description='validation tools',
      url='https://github.com/Ivanukh/validity',
      author='Yaroslav Ivanukh',
      author_email='Ya.Ivanukh@gmail.com',
      license='GPL',
      packages=['validity'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )
