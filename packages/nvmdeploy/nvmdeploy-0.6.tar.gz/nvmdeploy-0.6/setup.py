from setuptools import setup, find_packages

VERSION = '0.6'

setup(name='nvmdeploy',
      version=VERSION,
      description='fast release pod tool',
      long_description='fast release pod tool',
      classifiers=[],
      keywords='pod release',
      author='stephenw',
      author_email='zhilong.wang@ele.me',
      url='https://git.elenet.me/zhilong.wang/nvmdeploy',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'PyYAML',
          'python-jenkins'
      ],
      entry_points={
          'console_scripts': [
              'nvmdeploy = nvmdeploysrc.nevermore:entry'
          ]
      })