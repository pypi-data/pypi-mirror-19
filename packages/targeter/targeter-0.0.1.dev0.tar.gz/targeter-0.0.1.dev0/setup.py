from setuptools import setup, find_packages

setup(name='targeter',
      version='0.0.1',
      description=u"Utility for selecting files from a tree",
      classifiers=[],
      keywords='re, filesystem, utility',
      author=u"Julian Irwin",
      author_email='julian.irwin@gmail.com',
      url='https://github.com/julianirwin/retarget',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      setup_requires=['nose>=1.0'],
      extras_require={
          'test': ['nose'],
      },
      test_suite = 'nose.collector',
      entry_points = {
          'console_scripts': [],
          }
      )
