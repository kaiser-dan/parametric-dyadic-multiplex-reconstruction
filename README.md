# Multiplex Reconstruction with Partial Information

This project provides source code for the reconstruction of multiplex networks from partial structural observations. The repository also contains the original scientific analyses developed by the Authors (see below) for the paper

[D. Kaiser, S. Patwardhan, and F. Radicchi, Multiplex Reconstruction with Partial Information, Phys. Rev. E 107, 024309 (2023).](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.107.024309)


## Getting Started

The code base for this project is written in Python with package management handled with Conda.

These instructions will give you a copy of the project up and running on
your local machine for development, testing, and analysis purposes.

### Prerequisites

A compatible Python install is needed to begin - the package management is handled by Conda as described below.
- [Python \[3.10+\]](https://python.org/downloads/)
- [Conda \[ 4.14+\]](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html)

### Installing

To (locally) reproduce this project, do the following:

0. Download this code base. Notice that raw data are typically not included in the git-history and may need to be downloaded independently.
1. Open a terminal with Python and Conda installed and run the commands:
   ```
   $> conda env create -f environment.yaml
   $> conda activate NaiveDuplexReconstruction
   ```

This will install all necessary packages for you to be able to run the scripts and everything should work out of the box.

## Usage

We have elected to organize our code around the figures present in the [manuscript](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.107.024309). Various subdirectories under `experiments/` contain Jupyter notebooks titled `figureX.ipynb` (where X is some number 1-5 according to the subdirectory) which contain all relevant code to completely reproduce the experiments from the manuscript. Comments are available in the notebooks to describe source code.


## Built With
  - [ChooseALicense](https://choosealicense.com/) - Used to choose
    the license

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code
of conduct, and the process for submitting pull requests to us.

## Versioning

We use [Semantic Versioning](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/kaiser-dan/proj_sable-spin-duplexes/tags).

## Authors

All correspondence shoulld be directed to [Daniel Kaiser](mailto:kaiserd@iu.edu).

- Daniel Kaiser
- Siddharth Patwardhan
- Fillippo Radicchi

## License

This project is licensed under the [MIT License](LICENSE.md)
Creative Commons License - see the [LICENSE](LICENSE.md) file for
details

## Acknowledgments
  - **Billie Thompson** - *Provided README and CONTRIBUTING template* -
  [PurpleBooth](https://github.com/PurpleBooth)
