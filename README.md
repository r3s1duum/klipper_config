# Klipper Config

## Description

This repo stores the klipper configuration for my two printers:
- Ender3v2
- Voron2.4

## Prerequisites

- MainsailOS installation on a Raspberry Pi (3 or later)
- Clean `~/printer_data/config` folder
- Used `klipper` tag/version: `v0.13.0` 

> [!CAUTION]
> Use `residuum` for username, because the config is using the `/home/residuum`

## Installation

- Clone this repo into the `~/printer_data/config`
- Run `install.sh <printer_name>` use `--help` for more informations
- [Voron2.4]: Set up [klipper_z_calibration](https://github.com/protoloft/klipper_z_calibration)

