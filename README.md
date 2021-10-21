# Window To Viewport Mapper

[PT-BR Version](./README_pt_BR.md)

## Introduction

This Python program is a solution for what is requested in the [First Practical Work](./docs/TP1.pdf) of the Computer Graphics module of the Computer Science course at IFNMG.

The program reads a XML file containing data of the viewport and objects to be drawn, and performs a coordinate transformation for each object, mapping the object's original window-coordinate to a viewport-coordinate.

### Window To Viewport Transformation

To better understanding of window-to-viewport transformation, check the following explanation:

> "Window to Viewport Transformation is the process of transforming 2D world-coordinate objects to device coordinates. Objects inside the world or clipping window are mapped to the viewport which is the area on the screen where world coordinates are mapped to be displayed." - [Geeks For Geeks](https://www.geeksforgeeks.org/window-to-viewport-transformation-in-computer-graphics-with-implementation/)

<img src="./docs/window_viewport.jpg" alt="Window To Viewport Transformation" style="width: 600px">

## Running

### Prerequisites

- Python 3.10 or further version installed;
- A terminal with access to Python;
- PySide6 installed. You can install it running `pip install pyside6==6.2.0` in the terminal.

### Commands

Run `py src/main.py` or `python src/main.py` in the terminal.

The output file containing the viewport-coordinate of each object can be found in `data/output/viewport-coordinates.xml`.

## XML File (Input)

The input file already has some data defined. New data can be added if desired. The only requirement is that the `<viewport>` and `<window>` elements must keep the same format, and can only have their attribute values changed. Also, these two elements must be at the beginning of the XML root `<data>` tag, in the same original order.
