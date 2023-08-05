import glob
import json

from setuptools import setup, find_packages

with open('.project_metadata.json') as meta_file:
    project_metadata = json.loads(meta_file.read())


setup(
    name=project_metadata['name'],
    version=project_metadata['release'],
    author=project_metadata['author'],
    author_email=project_metadata['author_email'],
    description=project_metadata['description'],
    license=project_metadata['license'],
    install_requires=[],
    extras_require={
        'dev': [
            'pytest-capturelog',
            'pytest',
            'flake8',
        ],
    },
    include_package_data=True,
    packages=find_packages(),
    data_files=[
        ('icons', [
            'docs/_static/Dummy.ico',
            'docs/_static/Dummy.png',
        ])
    ],
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    scripts=glob.glob('bin/*'),
)
