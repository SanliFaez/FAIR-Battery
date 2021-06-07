
# Welcome to labphew!

![labphew logo](https://github.com/SanliFaez/labphew/blob/master/docs/source/_static/labphew_logo.png)

*labphew* is a minimalist code and folder structure for teaching computer-controlled lab instrumentation in Python. The main purpose of Labphew is to provide a basis for those with little coding experience to build their own user-interface(s) for a piece of hardware or to control a measurement and save their date in a properly reproducible manner.

### Python for the Lab

This project is heavily inspired by the instruction exercise written by [Dr. Aquiles Carattino](https://www.aquicarattino.com), the mastermind behind [Python for the Lab](https://www.pythonforthelab.com/). If you want to learn more (serious!) coding for lab automation with Python, check the excellent [PFTL website](https://www.pythonforthelab.com/) or book him for a course.

Python for the Lab (PFTL) is a code architecture and a programming course for computer-controlled instrumentation. PFTL codes are designed following the MVC design pattern, splitting the code into "controller"s for defining drivers, "model"s for specifying the logic of the experiment, and "view"s for parking the GUI.
PFTL was developed to explain to researchers, through simple examples, what can be achieved quickly with little programming experience. The ultimate goal of this project is to serve as a reference place for people interested in instrumentation written in Python.

## The labphew package

Currently, the labphew package contains more wishes than executable pieces. However you can use its framework as a (hopefully convenient) starting point to write your own code. Please note that this package is published under [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/). You can read all the available instruction on [labphew documentation](https://labphew.readthedocs.io/en/latest/)

## Hello world with mouse clicks

They are two recommended ways of installing labphew and using it out of the box:

### Installation from the Python package index

You need to have [pip](https://pypi.org/project/pip/) installed.

If affirmative, you can use:

    pip install labphew

### Installation from source

Building the labphew dependencies are tested on Windows and Mac PCs. It should be possible to install also on linux but we have not tested it yet.

    git clone https://github.com/sanlifaez/labphew.git
    cd labphew
    pip install .

If you want to start editing or adding to the code, we recommend that you fork the repository first to your own account and install it from there. This way of installation allows you to stay connected with the  labphew repository and when needed, rebase to future releases.

### Owning it

If you are ready to be more engaged and adapt labphew to control your own favorite setup, please read
[how to labphew](https://labphew.readthedocs.io/en/latest/howtolabphew.html).

## How to contribute

The labphew roadmap is still incomplete and actively discussed between its maintainers, @AronOpheij and @sanlifaez. If your interests are aligned with the main goals of this project and you want to get involved, you can send a few lines to Sanli.

