from setuptools import setup, find_packages

setup(
    name='download',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'requests', 'pillow'
    ],
    entry_points='''
        [console_scripts]
        download=app.download:parse
    ''',
)