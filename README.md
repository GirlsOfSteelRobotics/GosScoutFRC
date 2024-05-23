# GosScout
This repository contains FRC3504 The Girls Of Steel scouting analysis scripts.

## Getting Started

### Setup Development Environment
This project is written primarily in python, which you can install from [here](https://www.python.org/downloads/).

The recommended IDE to use is [PyCharm](https://www.jetbrains.com/pycharm/). We recommend installing it through [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/) So you can get notified of updates, and also easily install their other IDE's like IntelliJ for java.

### Installing Requirements
The scripts have several external dependencies. You can install them in bulk by running:

Windows:
`py -m pip install -r requirements.txt`

Linux / Mac:
`pip3 install -r requirements.txt`

## Intro Notebook
Jupyter Notebooks are a great way to play around with manipulating data, testing plots, and general experimentation. We have created an intro notebook with examples of how to slice dataframes and create simple plots.

The notebook can be viewed and edited in a browser. To start the server run this on the command line and open `intro.ipynb`
```commandline
jupyter notebook
```

## Shinny App
We use a Shinny App as our primary frontend for visualizing our scouting data. It can be started with
```commandline
shiny run .\app.py --reload
```

This will host a local website you can view in your browser at `http://127.0.0.1:8000`