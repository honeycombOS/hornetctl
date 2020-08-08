import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hornetctl-pkg-bernardoaraujor",
    version="0.0.1",
    author="Bernardo Araujo R.",
    author_email="bernardoaraujor@gmail.com",
    description="tools that help managing HORNET nodes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/honeycombOS/hornectctl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
