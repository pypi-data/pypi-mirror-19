from setuptools import setup

setup(name='getLatLng',
      version='1.0.0',
      description='Directory to get latitude and longitude values of particular city.',
      url='https://github.com/36rahu/pincode_directory',
      author='Piyush Wanare',
      author_email='piyushwanare24@gmail.com',
      license='MIT',
      zip_safe=False,
      packages=['getLatLng'],
      package_dir={'getLatLng': 'getLatLng/'},
      install_requires = ["requests"],
    )