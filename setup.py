import setuptools

setuptools.setup(
    name='git-conflict-finder',
    version='0.1.0',
    author='Geoff Mishkin',
    author_email='geoff@amsa.info',
    packages=['conflictfinder'],
    python_requires='>=3.6',
    install_requires=[
        'GitPython>=2.1,<3',
        'docopt>=0.6<1',
        'PyYAML>=5.1'
    ],
    extra_requires={
        'dev': ['pylint>=2.3']
    },
    entry_points={
        'console_scripts': [
            'find_conflicts=conflictfinder.cli:main'
        ]
    }
)
