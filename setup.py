import os
from setuptools import setup, find_packages

def get_version():
    version = {}
    with open(os.path.join("src", "cli", "__init__.py")) as f:
        exec(f.read(), version)
    print(version)
    return version["__version__"]

setup(
    # Basic project metadata
    name="askai",  # Name of the project
    version=get_version(),     # Version of the project
    author="UbaidManzoor",  # Author name
    author_email="ubaidmanzoor12@gmail.com",  # Author email
    description="A CLI tool powered by AI to help developers with code snippets.",  # Short description
    long_description=open("README.md").read(),  # Long description (from README.md)
    long_description_content_type="text/markdown",  # Format of the long description

    # Package discovery
    packages=find_packages(where="src"),  # Automatically find packages in the `src/` folder
    package_dir={"": "src"},  # Specify that packages are located in `src/`

    # Dependencies
    install_requires=[
        "requests>=2.31.0",  # Required dependencies
        "python-dotenv>=1.0.0",
    ],

    # Entry points (CLI commands)
    entry_points={
        "console_scripts": [
            "askai=cli.commands:main",  # Create a CLI command called `codesnip`
        ],
    },

    # Additional metadata
    url="https://github.com/yourusername/askai",  # Project URL
    classifiers=[  # Trove classifiers (for PyPI)
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version required
)