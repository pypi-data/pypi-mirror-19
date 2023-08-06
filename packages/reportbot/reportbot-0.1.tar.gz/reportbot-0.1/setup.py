

from setuptools import setup

setup(name='reportbot',
      version='0.1',
      description='report machine learning results to you on telegram',
      url='https://github.com/dotannn/reportbot',
      author='Dotan Asselmann',
      author_email='dotan1988@gmail.com',
      license='MIT',
      keywords=['roc', 'sklearn', 'classification', 'report', 'ml'],
      packages=['reportbot'],
      install_requires=[
            'telegram',
      ],
      zip_safe=False)
