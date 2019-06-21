from setuptools import setup


install_requires=[
    'benchmark-templates==0.1.1'
]


tests_require = [
    'coverage>=4.0',
    'coveralls',
    'nose'
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
    version='0.1.0',
    description='Simple Workflow Engine for Reproducible Benchmark Templates',
    keywords='reproducibility benchmarks data analysis',
    license='MIT',
    packages=['benchproc'],
    include_package_data=True,
    test_suite='nose.collector',
    extras_require=extras_require,
    tests_require=tests_require,
    install_requires=install_requires
)
