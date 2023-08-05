from setuptools import setup

setup(
    name='comicfetcher',
    version='0.3',
    description='Lets you fetch memes and comics',
    url='https://github.com/lakshaykalbhor/comic-fetcher',
    author='Lakshay Kalbhor',
    author_email='lakshaykalbhor@gmail.com',
    license='MIT',
    packages=['comicfetcher'],
    install_requires=[
        'bs4',
        'requests',
        'six',
        'argparse',
  ],
    entry_points={
        'console_scripts': ['comicfetcher=comicfetcher.command_line:main'],
    },
)
