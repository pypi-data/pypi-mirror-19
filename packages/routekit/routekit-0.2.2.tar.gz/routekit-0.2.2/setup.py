from setuptools import setup, find_packages

setup(
    name='routekit',
    description='Persistent policy routing and TC configuration toolkit for Linux',
    version='0.2.2',
    author='Timo Beckers',
    author_email='timo@incline.eu',
    url='https://github.com/ti-mo/routekit',
    keywords=['router','netlink','pyroute2'],
    py_modules=['routekit_cli'],
    packages=find_packages(),
    tests_require=['pytest', 'pytest-cov'],
    setup_requires=['pytest-runner'],
    install_requires=[
        'pyyaml',
        'python-consul',
        'pyroute2',
        'click',
        'netaddr',
        'colorama',
    ],
    entry_points='''
        [console_scripts]
        routekit=routekit_cli:cli
    ''',
    classifiers  = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration'
    ]
)
