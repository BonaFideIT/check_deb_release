# check_deb_release
[![Tests](https://github.com/bonafideit/check_deb_release/actions/workflows/tests.yml/badge.svg)](https://github.com/bonafideit/check_deb_release/actions/workflows/tests.yml)

A Nagios/Icinga plugin to monitor the installed Debian or Ubuntu release against a specified target (e.g., "stable").

## installation

`pip install check-deb-release`

## usage

```
usage: check_deb_release [-h] [--mirror MIRROR] [TARGET]

Nagios plugin to monitor if the currently running release of debian matches the desired target distribution

positional arguments:
  TARGET           Default: "stable", supported: "oldoldstable", "oldstable", "stable", "testing", "experimental"

options:
  -h, --help       show this help message and exit
  --mirror MIRROR  Debian Mirror to use as release reference. Default: https://deb.debian.org/debian/
```

## contributions

Install locally:

* fork
* clone
* create/checkout feature branch
* optional: virtual env
* install uv
* uv sync --dev
* **do work**
* create pull request where all tests pass
* changes will be merged after careful review

Run tests:

`uv run pytest`

Works for:

* debian bullseye
* debian bookworm

Does not currently work:

* debian buster ~ due to broken dependencies for old python version
