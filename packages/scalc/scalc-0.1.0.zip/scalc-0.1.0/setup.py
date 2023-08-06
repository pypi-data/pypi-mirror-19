from distutils.core import setup

setup(
    name = 'scalc',
    version = '0.1.0',
    description = 'A Python package example',
    author = 'Sailendra Pinupolu',
    author_email = 'spinupol@gmail.com',
    url = 'https://github.com/spinupol/scalc', 
    py_modules=['scalc'],
    install_requires=[
        # list of this package dependencies
    ],
    entry_points='''
        [console_scripts]
        scalc=scalc:cli
    ''',
)