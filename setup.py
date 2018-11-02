import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kai_python_package",
    version="0.0.1",
    author="Kai Software",
    author_email="tarush@vicara.co",
    description="A python package to use the sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CallMeTarush/kai_python_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)