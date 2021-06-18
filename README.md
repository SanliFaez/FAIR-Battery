# FAIR-Battery

[![Join the chat at https://gitter.im/FAIR-Battery/community](https://badges.gitter.im/FAIR-Battery/community.svg)](https://gitter.im/FAIR-Battery/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Software and design for building an open-hardware redox-flow battery from the Center for Unusual Collaborations [CUCo]

## Battery Hardware

[WIP]

## How to Test Batteries

A standard procedure for testing FAIR-Batteries has been developed. The main purpose of this standardization is to make
results much easier to compare. In order to achieve this, both software and hardware has been developed to fit the
testing needs of redox-flow batteries.

### Software for Battery Testing

The software works on any major computer platform, and binaries can be found here:
[Link to download of binaries]

The software is a fork of the Labphew project: https://github.com/SanliFaez/labphew.

### Hardware for Battery Testing

The battery testing software is currently designed around specific hardware, namely a Digilent Analog Discovery 2 (AD2),
a custom charging and discharging circuit, and for impedance spectroscopy, the Analog Discovery Impedance Analyzer
Module, an extension compatible with the AD2. 
