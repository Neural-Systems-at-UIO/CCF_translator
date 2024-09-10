from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="CCF_translator",
    version="0.2",
    packages=find_packages(),
    license="MIT",
    description="a package to translate data between common coordinate templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"CCF_translator": ["metadata/translation_metadata.csv"]},
    include_package_data=True,
    install_requires=["numpy", "nibabel", "scipy", "networkx", "pandas", "requests"],
)