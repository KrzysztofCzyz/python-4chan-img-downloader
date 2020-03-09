from setuptools import setup

setup(
    name='download',
    version='0.1',
    py_modules=['download'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        download=download:cli
    ''',
)