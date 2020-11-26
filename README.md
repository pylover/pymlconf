# pymlconf

[![PyPI](http://img.shields.io/pypi/v/pymlconf.svg)](https://pypi.python.org/pypi/pymlconf)
[![Build](https://github.com/pylover/pymlconf/workflows/Build/badge.svg?branch=master)](https://github.com/pylover/pymlconf/actions)
[![Coverage Status](https://coveralls.io/repos/github/pylover/pymlconf/badge.svg?branch=master)](https://coveralls.io/github/pylover/pymlconf?branch=master)
[![Documentation](https://img.shields.io/badge/Documentation-Ready-green.svg)](https://pylover.github.io/pymlconf)


## About

`pymlconf` (Python YAML Configuration Library) helps to easily manage
and access to your application configurations which was already Written
in [YAML](http://pyyaml.org) language.

Checkout [Documentation](https://pylover.github.io/pymlconf) for more info.


### Installation


```bash
pip install pymlconf
```

### Development

```bash
cd path/to/pymlconf
pip install -e .
pip install -r requirements-dev.txt
```

#### Running tests

```bash
pytest
```

#### Coverage

```bash
pytest --cov=pymlconf
```

#### Documentation

```bash
cd sphinx
make doctest
```

```bash
make html
or
make livehtml
```

