# Klipper configuration

## Description

My own klipper configuration for my following printers:
- Voron2.4
- Ender3 v2

## Prerequisites

- Klipper install on a Raspberry Pi
  - Username: residuum

## Development

### Setup

The formatting tool lives in `klipper_format/` and is installed into a virtual environment:

```sh
python3 -m venv .venv
.venv/bin/pip install -e .
```

### Format check (pre-commit)

A git pre-commit hook in `.githooks/` checks the staged text files with `klipper-format`. The commit is blocked if a file breaks the rules: trailing whitespace, CRLF line endings, tabs in indentation, indents that are not 2 spaces (4 for `.py`), or a missing or doubled final newline.

Enable it once per clone:

```sh
git config core.hooksPath .githooks
```

### Formatting all files

To check or fix every tracked file:

```sh
.venv/bin/klipper-format --check   # report problems only
.venv/bin/klipper-format           # fix in place
```

Pass file names instead to limit the run to those files.
