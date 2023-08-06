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
        'pandas >=0.15.2',
        'numpy >= 1.9.2',
        'matplotlib >= 1.4.3',
      ],

      zip_safe=False,
     )