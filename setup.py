from distutils.core import setup
import glob
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="irods_avu_json",
    version="2.2.0",
    author="Maastricht University - DataHub",
    author_email="datahub@maastrichtuniversity.nl",
    description="Bidirectional conversion between JSON(-LD) and iRODS AVUs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaastrichtUniversity/irods_avu_json",
    packages=['jsonavu'],
    scripts=['conversion.py'],
    data_files=[('test', glob.glob('test/*py')),
                ('inputs', glob.glob('inputs/*json')),
                ('LICENSE.md', ['LICENSE.md']),
                ('README.md', ['README.md']),
                ('jsonavu', glob.glob('jsonavu/*py'))],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ],
)
