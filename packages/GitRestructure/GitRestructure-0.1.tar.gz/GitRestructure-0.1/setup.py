from setuptools import setup, find_packages

setup(
    name='GitRestructure',
    version='0.1',
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
        res=restructure.res:cli
    ''',
)
