# Numbers2Words Greek

[![PyPI](https://img.shields.io/pypi/v/Numbers2Words-Greek.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/Numbers2Words-Greek.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/Numbers2Words-Greek)][python version]
[![License](https://img.shields.io/pypi/l/Numbers2Words-Greek)][license]

[![Read the documentation at https://Numbers2Words-Greek.readthedocs.io/](https://img.shields.io/readthedocs/Numbers2Words-Greek/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/geoph9/Numbers2Words-Greek/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/geoph9/Numbers2Words-Greek/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/Numbers2Words-Greek/
[status]: https://pypi.org/project/Numbers2Words-Greek/
[python version]: https://pypi.org/project/Numbers2Words-Greek
[read the docs]: https://Numbers2Words-Greek.readthedocs.io/
[tests]: https://github.com/geoph9/Numbers2Words-Greek/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/geoph9/Numbers2Words-Greek
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features


This repository contains code for converting converting numbers 
to words (e.g. 10 -> δέκα) up until `10^13 - 1` (1 trillion minus one).

- Convert numbers to greek words.
- Support for ordinals.
- Support for certain time formats.

## Installation:


You can install _Numbers2Words Greek_ via [pip] from [PyPI]:

```console
$ pip install Numbers2Words-Greek
```

If using `poetry`, then you can do `poetry add Numbers2Words-Greek`.

To install this repository locally, in editable mode, do the following:

```
git clone https://github.com/geoph9/Numbers2Words-Greek.git
cd Numbers2Words-Greek
pip install -e .
```

If no error occurs then you are fine. To make sure, you may run: 
`python -c "import num2word"`.

## Usage

### The `numbers2words.py` script:
This script contains functionality to convert numbers to their
corresponding words in Greek. It only handles positive numbers 
(you can easily change it to handle negative ones) and can also 
handle decimals (only if the decimal part is separated using "," 
instead of ".") and hours (e.g. 2:30 -> δύο και μισή). It is 
important to note that this algorithm does not take into account 
the gender of the noun following each number.
Also, the numbers will be converted as is and there is **no** 
post-processing like "2.5 ευρώ" -> "δυόμιση ευρώ" (the output 
will be "δύο κόμμα πέντε ευρώ").

If you only need to convert numbers to words then you may use this 
script as described below:

`python -m num2word [--test-word <<WORD>>] [--path <<PATH>>] 
[--extension .lab] [--out-path]`

Arguments:
- `-t` or `--test-word`: Use this only for testing. Put a word or 
number after it and check the result.
  E.g. `python -m num2word -t 150` should print `εκατόν πενήντα`.

- `-p` or `--path`: Provide a valid path. The path must be either a text file 
or a directory containing many files (the extension of these files is defined 
by the `-e` or `--extension` option, defaults to `.txt`). Cases:
    1. *Directory*: Inside this directory there needs to be multiple 
    text files which you want to convert. The words inside the file will 
    not be change and only the numbers will be replaced by their 
    corresponding words.
    2. *File*: If you provide a file then the same thing will happen but 
    just for this file.
- `-e` or `--extension`: Use this to change the extension of the text 
files you have provided in `--path`. This only matters if you have 
provided a directory. 

Example:

```
# num2word is the package and numbers2words.py is the script.
python -m num2word --path /home/user/data/transcriptions \
                   --extension .txt
```

The above will read all the `.txt` files inside the `transcriptions` 
directory and will change the numbers to their corresponding greek words.

---

## Future Work:

1. Handle fractions in `numbers2words`. E.g. Convert "1/10" to "ένα δέκατο".
2. Handle time input in `numbers2words`. E.g. Convert "11:20" to "έντεκα και είκοσι"


## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Numbers2Words Greek_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/geoph9/Numbers2Words-Greek/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/geoph9/Numbers2Words-Greek/blob/main/LICENSE
[contributor guide]: https://github.com/geoph9/Numbers2Words-Greek/blob/main/CONTRIBUTING.md
[command-line reference]: https://Numbers2Words-Greek.readthedocs.io/en/latest/usage.html
