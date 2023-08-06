from setuptools import setup, Extension

setup(
    name='gc-game-account-aggregator',
    version='1.0.1',
    author='Alex Etling',
    author_email='alex@gc.com',
    packages=['aggregator'],
    package_dir={'': '.'},
    zip_safe=False,
    url='https://github.com/gamechanger/game-account-aggregator',
    ext_modules = [Extension("aggregator/game_account_aggregator", ["aggregator/game_account_aggregator.c"])]
)