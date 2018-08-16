from setuptools import setup, find_packages

requires = [
    'beautifulsoup4',
    'requests'
]

setup(
    name='scholarium.analyzer',
    version='0.0.1',
    author='Philipp Bogensberger',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    extras_require={
        'test': []
    },
    entry_points={
        'console_scripts': [
            'download=scholarium.download:main',
        ]
    }
)
