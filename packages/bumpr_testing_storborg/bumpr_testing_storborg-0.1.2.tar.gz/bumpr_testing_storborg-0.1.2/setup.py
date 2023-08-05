from __future__ import print_function

from setuptools import setup, find_packages


setup(name='bumpr_testing_storborg',
      version='0.1.2',
      description='Testing bumpr.rc',
      long_description='',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='bumpr test',
      url='https://github.com/storborg/bumpr_testing_storborg',
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      license='GPL',
      packages=find_packages(),
      install_requires=[
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      include_package_data=True,
      zip_safe=False)
