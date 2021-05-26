from setuptools import setup, find_packages

VERSION = '0.1.0' 
DESCRIPTION = 'Package to enable easier worflows for variational quantum algorithms using qiskit'


def readme():
    with open('README.md') as f:
        return f.read()

# Setting up
setup(
        name="volta", 
        version=VERSION,
        description=DESCRIPTION,
        author="Nahum Sá",
        author_email="nahumsaa@gmail.com",
        long_description=readme(),
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=["qiskit>=0.25.0"], 
        url="https://github.com/nahumsa/volta",
        project_urls={
            "Bug Tracker": "https://github.com/nahumsa/volta/issues",
            "Source Code": "https://github.com/nahumsa/volta",
        },
        keywords=['python', 'quantum computing'],
        classifiers= [
            "License :: OSI Approved :: Apache Software License",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ]
)