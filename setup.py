from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
        name="bdf2ttf",
        version="0.0.1",
        author="Gabriel Holodak",
        description="Convert bitmap fonts into TTF format",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=["bdflib"],
        python_requires='>=3',
        entry_points={
            "console_scripts": [
                "bdf2ttf=bdf2ttf.convert:main"
                ]
            },
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            ]
        )
