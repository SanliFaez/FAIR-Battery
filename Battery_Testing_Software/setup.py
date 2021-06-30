from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

DESCRIPTION = "Fun with computer-controlled experiments for beginners"  # test to see if this description is picked up by conda environment manager

setup(

    name="labphew",
    version="0.3.2",

    packages=find_packages(),
    url="https://github.com/sanlifaez/labphew",
    license='GPLv3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    author='Sanli Faez, Aron Opheij',
    author_email='s.faez@uu.nl',
    description='Fun with computer-controlled experiments for beginners',
    long_description=long_description,

    long_description_content_type="text/markdown",
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'labphew = labphew.__main__:main'
        ],
    },
    install_requires=[
        'pint',
        'pyqt5==5.13.2',
        'pyqtgraph',
        'numpy',
        'PyYAML',
        'pyserial',
        'dwf',          # for Digilent WaveForms devices
        'xarray',       # (to save in netcdf4 format, xarray requires scipy or netcdf4)
        'scipy',
    ],
)
