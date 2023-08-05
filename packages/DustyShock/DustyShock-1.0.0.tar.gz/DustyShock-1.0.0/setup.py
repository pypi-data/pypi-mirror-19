from setuptools import setup, find_packages

setup(name='DustyShock',
      version='1.0.0',
      description='Two-fluid dusty gas shocks.',
      long_description='Two-fluid dusty gas shocks as benchmarking problems for numerical codes that simulate dusty gas. The two shock solutions are C-type and J-type shocks, as discussed in the soon to be submitted paper by Lehmann and Wardle.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Astronomy',
      ],
      keywords='Dust shocks ISM',
      author='Andrew Lehmann',
      author_email='andrew.lehmann.35@gmail.com',
      license='Apache',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
