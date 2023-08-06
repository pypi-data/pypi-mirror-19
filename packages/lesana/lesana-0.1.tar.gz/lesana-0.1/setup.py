from setuptools import setup, find_packages
setup(
    name='lesana',
    version='0.1',
    packages=find_packages(),
    scripts=['scripts/lesana'],

    install_requires=[
        'guacamole',
        # 'xapian >= 1.4',
        'ruamel.yaml',
        'jinja2',
        ],

    package_data={
        '': ['*.yaml']
        },
    test_suite='tests',

    # Metadata
    author="Elena ``of Valhalla'' Grandi",
    author_email='valhalla@trueelena.org',
    description='Manage collection inventories throught yaml files.',
    license='GPLv3+',
    keywords='collection inventory',
    url='https://lesana.trueelena.org/lesana',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        ],
)
