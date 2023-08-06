import os.path
from setuptools import find_packages, setup

version = open(os.path.join('plumbium', 'VERSION')).read().strip()


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='plumbium',
    version=version,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=True,
    author='Jon Stutters',
    author_email='j.stutters@ucl.ac.uk',
    description='Records the inputs and outputs of scripts',
    long_description=readme(),
    url='https://github.com/jstutters/plumbium',
    install_requires=['wrapt'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Logging'
    ]
)
