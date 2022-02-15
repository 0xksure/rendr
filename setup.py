from setuptools import setup, find_packages

setup(
    name='rendr',
    description='Server side rendering framework for python with a svelte like interface'
    author='Kristoffer Berg'
    version='0.0.1',
    packages=find_packages(where='src'),
    install_requires=[
        'requests',
        'importlib; python_version == "3.9"',
    ],
    python_requires='>=3.6, <4',
)
