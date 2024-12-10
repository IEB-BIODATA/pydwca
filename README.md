<picture align="center">
  <img alt="PyDwCA Logo" src="https://raw.githubusercontent.com/IEB-BIODATA/pydwca/refs/heads/develop/docs/source/favicon.png">
</picture>

-----------------

# Python DWCA

[![pypi](https://img.shields.io/pypi/v/pydwca?style=plastic&logo=pypi)](https://pypi.org/project/pydwca/)
![pypi-python-version](https://img.shields.io/pypi/pyversions/pydwca?style=plastic&logo=python)
![pypi-download](https://img.shields.io/pypi/dm/pydwca?style=plastic&logo=pypi)
![wheel](https://img.shields.io/pypi/wheel/pydwca?style=plastic)

[![issues](https://img.shields.io/github/issues/IEB-BIODATA/pydwca?style=plastic&logo=github)](https://github.com/IEB-BIODATA/pydwca/issues)
[![coverage](https://img.shields.io/codecov/c/github/IEB-BIODATA/pydwca?style=plastic&logo=codecov)](https://app.codecov.io/gh/IEB-BIODATA/pydwca)
[![licence](https://img.shields.io/github/license/IEB-BIODATA/pydwca?style=plastic)](https://www.mozilla.org/en-US/MPL/2.0/)

PyDwCA (pronounced /pajˈðjuka/ or _"pie thew ka"_) is a Python library to read, parse and write Darwin Core Archive files.

## Install

Package available at [pypi](https://pypi.org/project/pydwca/):

```shell
pip install pydwca
```

This command will install the library and the dependencies listed in the [`requirements`](requirements.txt). This will give you a basic usage.

If you want all the available features, install the optional dependencies:

```shell
pip install pydwca[full]
pip install pydwca[ui]
pip install pydwca[data]
```

`full` has all features, `ui` allows you to see the steps of the long process and `data` includes the libraries for data analysis. 

## Citation

You can cite this library by citing the abstract of the oral presentation in which was presented:

```
@article{10.3897/biss.8.137799,
	author = {Sáez-Hidalgo, Juan M. and Segovia, Ricardo A. and Squeo, Francisco A. and Guerrero, Pablo C.},
	title = {PyDwCA: A Tool for Integrating Biodiversity Data},
	volume = {8},
	number = {},
	year = {2024},
	doi = {10.3897/biss.8.137799},
	publisher = {Pensoft Publishers},
	issn = {},
	pages = {e137799},
	URL = {https://doi.org/10.3897/biss.8.137799},
	eprint = {https://doi.org/10.3897/biss.8.137799},
	journal = {Biodiversity Information Science and Standards}
}
```

## Usage

To read a DwC Archive file in `.zip` format, use the class `DarwinCoreArchive`:

```python
from dwca import DarwinCoreArchive

darwin_core = DarwinCoreArchive.from_archive("DwCArchive.zip")
```

A more extended example is in the library documentation at [https://pydwca.readthedocs.io/en/latest/usage.html](https://pydwca.readthedocs.io/en/latest/usage.html).

A more detailed example can be found on the [`pydwca-example`](https://github.com/IEB-BIODATA/pydwca-examples) repository. Those use cases correspond mainly to the data process pipeline presented at the 2024 SPNCH/TDWG conference.

## Documentation

Documentation is available at [readthedocs.io](https://pydwca.readthedocs.io/en/latest/index.html).

## Discussion

You can leave a message about the usage of this library, its implementation, or any other in the [issue section](https://github.com/IEB-BIODATA/pydwca/issues).
