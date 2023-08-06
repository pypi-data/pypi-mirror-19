from distutils.core import setup

setup(
  name = 'emergenSEE',
  packages = ['emergenSEE'],
  version = '0.6',
  description = 'Visualize NYC EMS Emergencies',
  author = 'Max Mattioli',
  author_email = 'm.max@columbia.edu',
  url = 'https://github.com/m-a-x/emergenSEE',
  download_url = 'https://github.com/m-a-x/emergenSEE/tarball/0.6',
  license='MIT',
  include_package_data=True,
  install_requires=['pandas>=0.19.1', 'numpy>=1.11.3', 'matplotlib>=1.5.3', 'descartes>=1.0.2', 'scikit-learn>=0.18.1', 'imageio==1.6'],
  classifiers = []
)
