import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kai-sdk",
    version="0.0.7",
    author="Vicara",
    author_email="dev@vicara.co",
    description="A python package to assist in interfacig with the KAI SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vicara-hq/kai-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)