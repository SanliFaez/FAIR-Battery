# The FAIR-Battery project

[![Join the chat at https://gitter.im/FAIR-Battery/community](https://badges.gitter.im/FAIR-Battery/community.svg)](https://gitter.im/FAIR-Battery/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


Hardware, design, and a learning community for building an open-hardware redox-flow battery from the [Center for Unusual Collaborations](https://www.unusualcollaborations.com/)

![FAIR-Battery logo](https://github.com/SanliFaez/FAIR-Battery/blob/main/docs/_static/fair-battery_logo.png)

In the _FAIR-Battery_ project, we aim to create an open-source electrochemical battery (FAIR = Findable + Accessible + Interoperable + Reproducible).
We seek to present an open-hardware platform for a versatile battery technology and make the platform radically accessible:
1- by deliberately using low cost and locally available materials suitable for local user groups, and
2- by setting up the education communities on top of the open-hardware design.

On this route, we thrive to not only provides the necessary technical details for engineering and production, but also incorporates the local constraints for actually adopting and using the technology.
These constraints relate to language, availability of materials and expertise, maintenance capacity, or other locally varying conditions, which must be identified as part of the project.
Our envisioned FAIR-Battery platform will track and seek to remove these constraints in each stage of the development by direct consultation with the user-groups.


Table of contents:

- [About the project](#about-the-project)
- [The team](#the-team)
- [Contributing](#contributing)
- [Get in touch](#get-in-touch)
- [Project pillars](#project-pillars)


## About the project

## The team

### Founding members

This project is initiated by:

- [Sanli Faez](sanlifaez.github.io/) - Utrecht University
- [Antoni Forner-Cuenca](https://www.fornercuencaresearch.com/) - Technical University of Eindhoven
- [Peter Ngene](https://www.uu.nl/staff/PNgene) - Utrecht University
- [Maarten Voors](https://www.wur.nl/nl/Personen/Maarten-dr.ir.-MJ-Maarten-Voors.htm) - Wageningen University
- [Yali Tang](https://www.tue.nl/en/research/researchers/yali-tang/) - Technical University of Eindhoven
- [Stephanie Hobbis](https://stephaniehobbis.com/) - Wageningen University

### Active students

The following students are currently contributing to the project

- Catherine Doherty - University College Utrecht
- Nicolas Barker - Delft University of Technology
- Emre Burak Boz - Technical University of Eindhoven

### Funding
FAIR-Battery is supported by a SPARK grant from the center for unusual collaborations.

## Contributing

:construction: This repository is always a work in progress and **everyone** is encouraged to help us build something that is useful to the many. :construction:

We are currently setting up the on-boarding instructions for persistent contributors.

The github issues and pull-request functions are currently _not_ actively used for updates.
These will be incorporate into the development procedures at a later stage

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification.
Contributions of any kind are welcome!

## Get in touch

If you wish to learn more about the project and/or join our learning community, drop an email to [Sanli Faez](mailto:s.faez@uu.nl)

## Project pillars

In our vision, to create a truly accessible FAIR-Battery, we need to form a community, at the same time that we collect and share the technical knowledge necessary for making and maintaining an operational device.
Therefore, we are building our activities on three pillars

### 1- Learning together

In this project, we will bring anthropologists, engineers, chemists,
 economists, and potential local users together to identify the barriers to developing a truly FAIR-battery and envision the first steps to removing some of these barriers in a follow-up project.
In particular, we look for the answers to these questions:
- What range of energy storage capacities are required for the development of typical user-groups and at what cost?
- Which battery technologies can potentially address these demands?
- Are the materials and technologies required for adopting the identifies technologies available in the identifies user-groups? If not, which adjustments are needed?
- What is the missing know-how and expertise for kick-starting the local development of pilot projects?

For investigating these questions, together with an inclusive community, we will develop:
- A. a starters' kit (hardware and software)
- B. a lecture series for self-study


### 2- Battery Hardware

Our aim is to publish the blueprints for an operational open-source battery by July 2022.
We will regularly report on the devices that we are using for intermediate steps, such as testing and material selection, on this repository.

### 3- Testing and Maintenance

A standard procedure for testing FAIR-Batteries is currently being developed. The main purpose of this standardization is to make
results from different contributing groups easy to compare. In order to achieve this, both software and hardware has been developed to fit the testing needs of redox-flow batteries.

_Software for Battery Testing_

We have developed an open-srouce python code that works on any major computer platform.
You can check the installation guide and further documentation on [readthedocs](https://fair-battery.readthedocs.io/en/latest/index.html).

The software is a fork of the Labphew project: https://github.com/SanliFaez/labphew.

### Hardware for Battery Testing

The battery testing software is currently designed around specific hardware, namely a Digilent Analog Discovery 2 (AD2),
a custom charging and discharging circuit, and for impedance spectroscopy, the Analog Discovery Impedance Analyzer
Module, an extension compatible with the AD2. 

