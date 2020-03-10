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
        download=app.download:cli
    ''',
)

# setup(
#     name='test-download',
#     version='0.1',
#     packages=find_packages(),
#     install_requires=[
#         'Click', 'requests', 'pillow'
#     ],
#     entry_points='''
#         [console_scripts]
#         test-download=test.download-test:test_all
#     '''
# )
