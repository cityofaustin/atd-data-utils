import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdutils",
    version="0.0.15",
    author="City of Austin",
    author_email="transportation.data@austintexas.gov",
    description="Various utilities for managing and pulishing transportation data.",
    install_requires=[
      'arrow',
      'requests',
      'arcgis',
      'pymssql',
      'yagmail'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cityofaustin/transportation-data-utils",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta", 
    ),
)

