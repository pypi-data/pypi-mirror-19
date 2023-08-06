from setuptools import setup

from pythonToolbox.version import __version__


setup(name='aquanToolbox',
      version=__version__,
      description='The Auquan Toolbox for trading system development',
      url='http://auquan.com/',
      author='Auquan',
      author_email='info@auquan.com',
      license='MIT',
      packages=['pythonToolbox'],
      scripts=['TradingStrategyTemplate', 'MeanReversion', 'BollingerBand'],
      include_package_data = True,

      install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
      ],

      zip_safe=False,
     )