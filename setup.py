from setuptools import setup, find_packages


readme = open('README.rst').read()

install_requires=[
    'benchmark-templates>=0.1.2'
]


tests_require = [
    'coverage>=4.0',
    'pytest',
    'pytest-cov',
    'tox'
]


extras_require = {
    'docs': [
        'Sphinx',
        'sphinx-rtd-theme'
    ],
    'tests': tests_require,
}


setup(
    name='benchmark-multiprocess',
    version='0.1.2',
    description='Simple Workflow Engine for Reproducible Benchmark Templates',
    long_description=readme,
    long_description_content_type='text/x-rst',
    keywords='reproducibility benchmarks data analysis',
    url='https://github.com/scailfin/benchmark-multiproc-backend',
    author='Heiko Mueller',
    author_email='heiko.muller@gmail.com',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    test_suite='nose.collector',
    extras_require=extras_require,
    tests_require=tests_require,
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python'
    ],
)
