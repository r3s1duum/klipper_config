#!/bin/bash
# Links printer.cfg in the root for the given printer and builds moonraker.conf
# from moonraker-common.conf plus the printer's moonraker-extra.conf.
# set -x
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

ender3v2="ender3v2"
voron24="voron2.4"
available_printers=($ender3v2 $voron24)

[[ -L "$SCRIPT_DIR/printer.cfg" ]] && unlink "$SCRIPT_DIR/printer.cfg"
[[ -L "$SCRIPT_DIR/moonraker.conf" ]] && unlink "$SCRIPT_DIR/moonraker.conf"

build_moonraker() {
  cat "$SCRIPT_DIR/moonraker-common.conf" "$SCRIPT_DIR/printers/$1/moonraker-extra.conf" > "$SCRIPT_DIR/moonraker.conf"
}

case $1 in
  $voron24)
    ln -s "$SCRIPT_DIR/printers/$voron24/printer.cfg" "$SCRIPT_DIR/printer.cfg"
    build_moonraker $voron24
    ;;
  $ender3v2)
    ln -s "$SCRIPT_DIR/printers/$ender3v2/printer.cfg" "$SCRIPT_DIR/printer.cfg"
    build_moonraker $ender3v2
    ;;
  --help)
    echo """Link the printer.cfg file and build moonraker.conf for the chosen printer. Available printers are: ${available_printers[*]}"""
    ;;
  *)
    echo "Wrong argument! Available printers are: ${available_printers[*]}"
    ;;
esac
