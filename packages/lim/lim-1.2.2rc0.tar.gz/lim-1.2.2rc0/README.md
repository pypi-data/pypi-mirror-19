# lim

[![PyPIl](https://img.shields.io/pypi/l/lim.svg?style=flat-square)](https://pypi.python.org/pypi/lim/)
[![PyPIv](https://img.shields.io/pypi/v/lim.svg?style=flat-square)](https://pypi.python.org/pypi/lim/)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/lim/badges/version.svg)](https://anaconda.org/conda-forge/lim)
[![Documentation Status](https://readthedocs.org/projects/lim/badge/?style=flat-square&version=latest)](http://lim.readthedocs.io/en/latest/?badge=latest)

Lim is an efficient implementation of Generalized Linear Mixed Models for
genomic analysis.

## Install

The recommended way of installing it is via
[conda](http://conda.pydata.org/docs/index.html)
```bash
conda install -c conda-forge lim
```
which requires having [Anaconda package](https://www.continuum.io/downloads)
installed beforehand. (Don't be shy, it is hassle-free.)

An alternative way would be via pip
```bash
pip install lim
```
which requires a deep understanding of Python packages and C libraries
dependency resolution.
This is not recommended for most users.

Refer to [documentation](http://lim.readthedocs.io/) for more information.

## Running the tests

After installation, you can test it
```
python -c "import lim; lim.test()"
```
as long as you have [pytest](http://docs.pytest.org/en/latest/).

## Authors

* **Christoph Lippert** - [https://github.com/clippert](https://github.com/clippert)
* **Danilo Horta** - [https://github.com/Horta](https://github.com/Horta)
* **Oliver Stegle** - [https://github.com/ostegle](https://github.com/ostegle)
* **Paolo Francesco Casale** - [https://github.com/fpcasale](https://github.com/fpcasale)

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details
