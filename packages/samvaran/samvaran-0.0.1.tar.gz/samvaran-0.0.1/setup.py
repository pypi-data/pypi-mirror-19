from distutils.core import setup

setup(
    name = 'samvaran',
    version = '0.0.1',
    description = 'A Python package example by samvaran',
    author = 'samvaran kashyap rallabandi',
    author_email = 'samvaran.kashyap@gmail.com',
    url = '', 
    py_modules=['samvaran'],
    install_requires=[
    # list of this package dependencies
    ],
    entry_points='''
                 [console_scripts]
                 samvaran=samvaran:cli
                 ''',
    )
