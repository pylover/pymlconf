# pymlconf

[![PyPI](http://img.shields.io/pypi/v/pymlconf.svg)](https://pypi.python.org/pypi/pymlconf)
[![Build](https://github.com/pylover/pymlconf/actions/workflows/build.yml/badge.svg)](https://github.com/pylover/pymlconf/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/pylover/pymlconf/badge.svg?branch=master)](https://coveralls.io/github/pylover/pymlconf?branch=master)
[![Documentation](https://img.shields.io/badge/Documentation-Ready-green.svg)](https://pylover.github.io/pymlconf)
[![Downloads](https://pepy.tech/badge/pymlconf)](https://pepy.tech/project/pymlconf)
[![Downloads](https://pepy.tech/badge/pymlconf/month)](https://pepy.tech/project/pymlconf)
[![Downloads](https://pepy.tech/badge/pymlconf/week)](https://pepy.tech/project/pymlconf)

## About

`pymlconf` (Python YAML Configuration Library) helps to easily manage
and access to your application configurations which was already Written
in [YAML](http://pyyaml.org) language.

Checkout [Documentation](https://pylover.github.io/pymlconf) for more info.


## Contribution

### python-makelib
Install [python-makelib](https://github.com/pylover/python-makelib).


### Virtualenv

Create virtual environment:
```bash
make venv
```

Delete virtual environment:
```bash
make venv-delete
```

Activate the virtual environment:
```bash
source ./activate.sh
```


### Install (editable mode)
Install this project as editable mode and all other development dependencies:
```bash
make env
```


### Tests
Execute all tests:
```bash
make test
```

Execute specific test(s) using wildcard:
```bash
make test F=tests/test_meld*
make test F=tests/test_meld.py::test_meld_merge
```

*refer to* [pytest documentation](https://docs.pytest.org/en/7.1.x/how-to/usage.html#how-to-invoke-pytest)
*for more info about invoking tests.*

Execute tests and report coverage result:
```bash
make cover
make cover F=tests/test_static.py
make cover-html
```


# Lint
```bash
make lint
```


### Distribution
Execute these commands to create `Python`'s standard distribution packages
at `dist` directory:
```bash
make sdist
make wheel
```


### Clean build directory
Execute: 
```bash
make clean
```
to clean-up previous `dist/*` and `build/*` directories.


### PyPI

> **_WARNING:_** Do not do this if you'r not responsible as author and 
> or maintainer of this project.

Execute
```bash
make clean
make pypi
```
to upload `sdists` and `wheel` packages on [PyPI](https://pypi.org).


## Documentation

```bash
source activate.sh
make doc
make doclive
make doctest
```

Or 

```bash
source activate.sh
cd sphinx
make doctest
make html
make livehtml
```
