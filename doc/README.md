# Dyadic multiplex reconstruction
[![Paper](http://img.shields.io/badge/paper-arxiv.1809.02589-B31B1B.svg)](https://arxiv.org/abs/1809.02589) 

## Overview
---

### What the algorithm does
Given a multiplex BLAH BLAH BLAH

### How to use it

DO THE THING

## Software Dependencies
---
This source code was written in Python3.8 and has minimal external dependencies, primarily concerning network datastructures and community detection algorithms. A full set of Python package requirements is given in `requirements.txt` with the main packages listed below.

- Python>=3.6
- networkx==2.7
- python-louvain==0.16
- numpy==1.22.2


## Installation and Usage
---
### Installation

To get this code on your own machine and use it effectively, you are able to follow the proceeding setup:

1. Get a an appropriate [Python](https://www.python.org/) installation (created in Python 3.8, tested on 3.6, 3.8-3.10.1).
2. If you are using a virtual environment (recommended), create a new environment. Using `venv` from the Python standard library, run the following from terminal
```bash
python3 -m venv path/to/venv
```
replaceing `bin` with `Scripts` if on Windows. 

3. Clone the repository with 
```bash 
git clone THING
cd THING
```

4. Activate the virtual environment and install the required dependencies with 
```bash 
source activate path/to/venv/bin/activate
pip install -r requirements.txt
```

That's it, you are installed and ready to go! The following section will detail how to use the code, including both what scripts to interract with, what configuration files to alter, and how to format your data.

### Usage

**HMMMMMMM**

Add your aggregate edgelist and partial observations into the `data/` directory. They must adhere to the format 

## Contributing
---

If you have have any ideas or suggestions on improving the algorithm or its implementation, please send us an email at any of the emails listed below!

If you see any _bugs_, however, please both send us an email and create a Github Issue on this repository according to the given template.

## Authors
---

The following are all authors, listed alphabetically by last name, on the associated paper. Those marked with an '*' contributing to the source code in this repository, and those marked with an '**' are corresponding programmer(s) for this repository.

- Daniel Kaiser** - kaiserd@iu.edu
- Siddharth Patwardhan* - sidpatwa@iu.edu
- Filippo Radicchi - filiradi@iu.edu


## Citation:
---

If you use this code in your work please cite the associated paper:

```bibtex

```
