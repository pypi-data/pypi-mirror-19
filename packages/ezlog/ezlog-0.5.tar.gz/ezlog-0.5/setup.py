from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='ezlog',
    packages=[
        'ezlog',
    ],
    package_dir={
        'ezlog': 'ezlog',
    },
    version='0.5',
    license="MIT license",
    description='Helpful wrappers for logging',
    long_description=readme,
    author='Eugene Ivanchenko',
    author_email='ez@eiva.info',
    url='https://github.com/eiva/ezlog',
    download_url='https://pypi.python.org/pypi/ezlog',
    keywords=['logging', 'wrapper', 'performance'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English'],
)
