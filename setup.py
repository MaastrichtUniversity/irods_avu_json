import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="irods_avu_json",
    version="0.1.0",
    author="Maastricht University - DataHub",
    author_email="datahub@maastrichtuniversity.nl",
    description="Bidirectional conversion between JSON(-LD) and iRODS AVUs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaastrichtUniversity/irods_avu_json",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)