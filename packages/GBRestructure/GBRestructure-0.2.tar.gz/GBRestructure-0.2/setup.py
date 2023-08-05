from setuptools import setup, find_packages

setup(
    name='GBRestructure',
    version='0.2',
    description='A CLI tool that helps collaborating teams restructure their git branching strategies',
    author='Josh Fischer',
    author_email='josh@joshfischer.io',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        gb=restructure.gb:cli
    ''',
)
