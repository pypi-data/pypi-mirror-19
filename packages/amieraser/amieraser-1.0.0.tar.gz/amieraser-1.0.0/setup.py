from setuptools import setup

setup(name='amieraser',
      version='1.0.0',
      description='Tool to delete Amazon AMIs and associated Snapshots',
      url='https://github.com/drboyer/AMIEraser',
      author='Devin Boyer',
      author_email='drb5272@gmail.com',
      license='MIT',
      packages=['amieraser'],
      install_requires=[
          'boto3',
      ],
      entry_points = {
          'console_scripts': ['amieraser=amieraser.amieraser:cli'],
      },
      zip_safe=False)